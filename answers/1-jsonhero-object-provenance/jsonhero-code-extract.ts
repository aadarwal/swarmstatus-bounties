/**
 * TriggerDev JSON Hero Architecture Extracts
 * Repository: triggerdotdev/jsonhero-web
 * Pinned Commit: 15157053174ba7a0a79c77b2925fbde7e05a6334
 * 
 * Relevant files demonstrating document data model, URL document storage,
 * dynamic fetching behavior, and document title propagation to the <title> tag.
 */

// ============================================================================
// File 1: app/jsonDoc.server.ts
// ============================================================================

export type BaseJsonDocument = {
  id: string;
  title: string;
  readOnly: boolean;
};

export type RawJsonDocument = BaseJsonDocument & {
  type: "raw";
  contents: string;
};

export type UrlJsonDocument = BaseJsonDocument & {
  type: "url";
  url: string;
};

export type JSONDocument = RawJsonDocument | UrlJsonDocument;

export type CreateJsonOptions = {
  title?: string;
  readOnly?: boolean;
  ttl?: number;
  metadata?: Record<string, string>;
  injest?: boolean;
};

export async function createFromRawJson(
  filename: string,
  contents: string,
  options?: CreateJsonOptions
): Promise<JSONDocument> {
  const docId = createId();

  const doc: JSONDocument = {
    id: docId,
    type: "raw",
    contents,
    title: filename,
    readOnly: options?.readOnly ?? false,
  };

  await DOCUMENTS.put(docId, JSON.stringify(doc), {
    expirationTtl: options?.ttl ?? undefined,
    metadata: options?.metadata ?? undefined,
  });

  return doc;
}

export async function createFromUrl(
  url: URL,
  title?: string,
  options?: CreateJsonOptions
): Promise<JSONDocument> {
  if (options?.injest) {
    const response = await fetch(url.href);
    const contents = await response.text();
    return createFromRawJson(title ?? url.hostname, contents, options);
  }

  const docId = createId();

  const doc: JSONDocument = {
    id: docId,
    type: "url",
    url: url.href,
    title: title ?? url.hostname,
    readOnly: options?.readOnly ?? false,
  };

  await DOCUMENTS.put(docId, JSON.stringify(doc), {
    expirationTtl: options?.ttl ?? undefined,
    metadata: options?.metadata ?? undefined,
  });

  return doc;
}

// ============================================================================
// File 2: app/routes/actions/createFromUrl.ts
// ============================================================================

export let loader: LoaderFunction = async ({ request, context }) => {
  const url = new URL(request.url);
  const jsonUrl = url.searchParams.get("jsonUrl");

  if (!jsonUrl) {
    return redirect("/");
  }

  const jsonURL = new URL(jsonUrl);
  // Note: createFromUrl is called with jsonURL.href as the title parameter!
  const doc = await createFromUrl(jsonURL, jsonURL.href);

  return redirect(`/j/${doc.id}`);
};

// ============================================================================
// File 3: app/routes/j/$id.tsx
// ============================================================================

export const meta: MetaFunction = ({ data }) => {
  let title = "JSON Hero";

  if (data?.doc?.title) {
    title += ` - ${data.doc.title}`;
  }

  return {
    title,
    "og:title": title,
    description: "JSON Hero is an open-source JSON viewer built for the web.",
    "og:description": "JSON Hero is an open-source JSON viewer built for the web.",
  };
};

export const loader: LoaderFunction = async ({ request, params }) => {
  const { id } = params;
  if (!id) {
    return redirect("/");
  }

  const doc = await get(id);
  if (!doc) {
    throw new Response("Not Found", { status: 404 });
  }

  const url = new URL(request.url);
  const path = url.searchParams.get("path");
  const minimal = url.searchParams.get("minimal") === "true";

  if (doc.type === "url") {
    // Fetches upstream doc.url dynamically on viewer request
    const jsonResponse = await safeFetch(doc.url, {
      headers: {
        "User-Agent": getRandomUserAgent(),
      },
    });

    if (!jsonResponse.ok) {
      return {
        doc,
        error: {
          title: "Could not fetch JSON",
          message: `Could not fetch JSON from ${doc.url}`,
        },
      };
    }

    const json = await jsonResponse.json();

    return {
      doc,
      json,
      path,
      minimal,
    };
  }

  return {
    doc,
    json: JSON.parse(doc.contents),
    path,
    minimal,
  };
};
