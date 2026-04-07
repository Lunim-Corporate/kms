import { useMemo, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [query, setQuery] = useState("");
  const [session, setSession] = useState("");
  const [category, setCategory] = useState("");
  const [meaningfulOnly, setMeaningfulOnly] = useState(true);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sessionOptions = useMemo(
    () => ["Tabb onboarding Mar 26", "Tab Opportunities Usability Testing"],
    []
  );

  const categoryOptions = useMemo(() => ["Tabb Community"], []);

  async function handleSearch(e) {
    e?.preventDefault();
    if (!query.trim()) return;

    const submittedQuery = query.trim();

    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${API_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: submittedQuery,
          session: session || null,
          category: category || null,
          meaningful_only: meaningfulOnly,
          top_k: 6,
        }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "Search failed");

      setResults(data.results || []);
      setQuery("");
    } catch (err) {
      setError(err.message || "Something went wrong");
    }  finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-screen overflow-hidden bg-[#0b1020] text-slate-100">
      <div className="flex h-full">
        <aside className="hidden h-full w-[300px] shrink-0 border-r border-white/10 bg-[#0f172a]/80 p-6 lg:flex lg:flex-col">
          <div>
            <div className="mb-3 inline-flex rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-300">
              Lunim • Knowledge Intelligence
            </div>
            <h1 className="text-2xl font-semibold tracking-tight text-white">
              Internal AI Search
            </h1>
            <p className="mt-2 text-sm leading-6 text-slate-400">
              Query organisational knowledge, surface insights, and trace back to source material.
            </p>
          </div>

          <div className="mt-8 space-y-5">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-300">
                Session
              </label>
              <select
                value={session}
                onChange={(e) => setSession(e.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200 outline-none focus:border-indigo-400"
              >
                <option value="">All sessions</option>
                {sessionOptions.map((item) => (
                  <option key={item} value={item} className="bg-slate-900">
                    {item}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm font-medium text-slate-300">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200 outline-none focus:border-indigo-400"
              >
                <option value="">All categories</option>
                {categoryOptions.map((item) => (
                  <option key={item} value={item} className="bg-slate-900">
                    {item}
                  </option>
                ))}
              </select>
            </div>

            <label className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={meaningfulOnly}
                onChange={(e) => setMeaningfulOnly(e.target.checked)}
                className="h-4 w-4 rounded border-slate-500 bg-transparent"
              />
              Only meaningful content
            </label>
          </div>

          <div className="sticky bottom-6 mt-8 rounded-2xl border border-white/10 bg-white/5 p-4 text-xs leading-6 text-slate-400 backdrop-blur">
            <div className="mb-2 font-semibold text-slate-300">Suggested prompts</div>

            <button
              onClick={() => setQuery("What onboarding issues did users face?")}
              className="mb-2 block w-full rounded-xl px-3 py-2 text-left text-slate-400 transition hover:bg-white/10 hover:text-white"
            >
              • What onboarding issues did users face?
            </button> 
            <button
              onClick={() => setQuery("What trust problems were mentioned?")}
              className="mb-2 block w-full rounded-xl px-3 py-2 text-left text-slate-400 transition hover:bg-white/10 hover:text-white"
            >
              • What trust problems were mentioned?
            </button>

            <button
              onClick={() => setQuery("What recommendations were made?")}
              className="block w-full rounded-xl px-3 py-2 text-left text-slate-400 transition hover:bg-white/10 hover:text-white"
            >
              • What recommendations were made?
            </button>
          </div>
        </aside>

        <main className="flex h-full flex-1 flex-col overflow-hidden">
          <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col overflow-y-auto px-4 py-8 md:px-8">
            {results.length === 0 && !loading && !error && (
              <div className="flex flex-1 items-center justify-center">
                <div className="max-w-2xl text-center">
                  <div className="mb-4 inline-flex rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-300 lg:hidden">
                    Lunim • Knowledge Intelligence
                  </div>
                  <h2 className="text-4xl font-semibold tracking-tight text-white md:text-5xl">
                    Ask anything about your internal research.
                  </h2>
                  <p className="mt-4 text-base leading-7 text-slate-400">
                    Search onboarding feedback, trust signals, usability pain points, and supporting evidence from organisational documents.
                  </p>
                </div>
              </div>
            )}

            {loading && (
              <div className="mb-6 rounded-3xl border border-white/10 bg-white/5 p-5 text-sm text-slate-300">
                Analyzing knowledge chunks...
              </div>
            )}

            {error && (
              <div className="mb-6 rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
                {error}
              </div>
            )}
            {results.length === 0 && !loading && !error && (
              <div className="flex flex-1 items-center justify-center">
                <div className="max-w-2xl text-center">
                  <div className="mb-4 inline-flex rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-300 lg:hidden">
                    Lunim • Knowledge Intelligence
                  </div>
                  <h2 className="text-4xl font-semibold tracking-tight text-white md:text-5xl">
                    Ask anything about your internal research.
                  </h2>
                  <p className="mt-4 text-base leading-7 text-slate-400">
                    Search onboarding feedback, trust signals, usability pain points, and supporting evidence from organisational documents.
                  </p>
                </div>
              </div>
            )}

            {loading && (
              <div className="mb-6 rounded-3xl border border-white/10 bg-white/5 p-5 text-sm text-slate-300">
                Analyzing knowledge chunks...
              </div>
            )}

            {error && (
              <div className="mb-6 rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
                {error}
              </div>
            )}

            {/* ❌ NO RESULTS */}
            {!loading && !error && results.length === 0 && (
              <div className="mb-6 rounded-3xl border border-white/10 bg-white/[0.04] p-8 text-center text-sm text-slate-400">
                No sufficiently relevant results found. Try a clearer or more specific question.
              </div>
            )}

            {!loading && !error && results.length > 0 && (
              <>
                <div className="mb-6 rounded-3xl border border-indigo-400/20 bg-gradient-to-br from-indigo-500/10 to-slate-900 p-6">
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-indigo-300">
                    AI Insight
                  </div>
                  <h2 className="text-xl font-semibold text-white">
                    Top answer from organisational knowledge
                  </h2>
                  <p className="mt-3 text-sm leading-7 text-slate-300">
                    Found {results.length} relevant results. The highest-ranking evidence appears below, with supporting chunks and traceable source attachments.
                  </p>
                </div>
                

                <div className="space-y-4 pb-32">
                  {results.map((result, index) => (
                    <details
                      key={`${result.title}-${index}`}
                      className="group rounded-3xl border border-white/10 bg-white/[0.04] p-6 transition hover:bg-white/[0.06]"
                    >
                      <summary className="cursor-pointer list-none">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <h3 className="text-xl font-semibold text-white">
                              {result.title}
                            </h3>

                            <div className="mt-3 flex flex-wrap gap-2">
                              <span className="rounded-full bg-indigo-500/15 px-3 py-1 text-xs font-medium text-indigo-300">
                                Session: {result.metadata?.session || "N/A"}
                              </span>
                              <span className="rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-slate-300">
                                Category: {(result.metadata?.category || []).join(", ") || "N/A"}
                              </span>
                              <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-medium text-emerald-300">
                                Score: {result.score}
                              </span>
                            </div>

                            <p className="mt-4 text-sm leading-7 text-slate-300">
                              {result.preview}...
                            </p>
                          </div>

                          <div className="pt-1 text-slate-500 transition group-open:rotate-180">
                            ⌄
                          </div>
                        </div>
                      </summary>

                      <div className="mt-6 border-t border-white/10 pt-6">
                        <h4 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
                          Full chunk
                        </h4>
                        <p className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
                          {result.text}
                        </p>

                        {result.files?.length > 0 && (
                          <div className="mt-6">
                            <h4 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
                              Attachments
                            </h4>
                            <div className="space-y-2">
                              {result.files.map((file, i) => (
                                <a
                                  key={`${file.name}-${i}`}
                                  href={file.url}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300 transition hover:bg-white/10"
                                >
                                  <span>{file.name}</span>
                                  <span className="text-slate-500">↗</span>
                                </a>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </details>
                  ))}
                </div>
              </>
            )}
          </div>

          <div className="sticky bottom-0 border-t border-white/10 bg-[#0b1020]/80 px-4 py-4 backdrop-blur md:px-8">
            <form onSubmit={handleSearch} className="mx-auto w-full max-w-4xl">
              <div className="flex gap-3 items-center bg-white/10 backdrop-blur rounded-2xl border border-white/10 px-4 py-3 shadow-sm focus-within:ring-2 focus-within:ring-indigo-400">
    
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="flex-1 outline-none text-sm bg-transparent text-white placeholder:text-slate-400"
                  placeholder="Ask about onboarding issues, trust concerns, or usability pain points..."
                />

                <button
                  type="submit"
                  className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 transition"
                >
                  Search
                </button>

              </div>
            </form>
          </div>
        </main>
      </div>
    </div>
  );
}