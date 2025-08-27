def build_index(chunk_size_words=200, overwrite=False):
    global _faiss_index, _meta
    _ensure_index_dir()
    if INDEX_FILE.exists() and META_FILE.exists() and not overwrite:
        return load_index()

    docs = []
    # Accept both .txt and .md files
    for p in sorted(BLOG_DIR.glob("*")):
        if p.suffix.lower() not in [".txt", ".md"]:
            continue
        raw = p.read_text(encoding="utf-8").strip()
        if not raw:
            continue
        words = raw.split()
        for i in range(0, len(words), chunk_size_words):
            chunk = " ".join(words[i:i+chunk_size_words])
            docs.append({"title": p.stem, "text": chunk})

    if not docs:
        raise ValueError("❌ No embeddings generated. Check blogs/ content!")

    model = _get_embed_model()
    texts = [d["title"] + "\n" + d["text"] for d in docs]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_FILE))
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"docs": docs}, f, ensure_ascii=False, indent=2)

    _faiss_index = index
    _meta = {"docs": docs}
    return index, _meta
