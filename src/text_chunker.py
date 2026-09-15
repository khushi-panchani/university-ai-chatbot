def split_text_into_chunks(text, chunk_size=500, chunk_overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)
        
        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks