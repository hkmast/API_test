from service import app
from flask import request, jsonify
from service.models import bm25_search, sbert_search


@app.route("/bm25", methods=["POST"])
def bm25():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(bm25_search.search(query=query, k=k))


@app.route("/sbert", methods=["POST"])
def sbert():
    data = request.get_json()
    query = data["query"]
    k = data["k"]
    return jsonify(sbert_search.search(query=query, k=k))


@app.route("/combinate", methods=["POST"])
def combinate():
    data = request.get_json()
    query = data["query"]
    k = data["k"]

    bm = bm25_search.search(query=query, k=k)["documents"]
    sb = sbert_search.search(query=query, k=k)["documents"]

    return jsonify({"result": RRF(bm, sb, k)})


def RRF(bm, sb, k):
    all_list = list(set([i.meta["name"] for i in bm] + [i.meta["name"] for i in sb]))
    print(all_list)
    res = []

    bm_dict = {}
    sb_dict = {}

    for i in range(k):
        b = bm[i]
        s = sb[i]

        if b.meta["name"] not in bm_dict:
            bm_dict[b.meta["name"]] = 1 / (i + 1)

        if s.meta["name"] not in sb_dict:
            sb_dict[s.meta["name"]] = 1 / (i + 1)

    # print(f"bm_dict: {bm_dict}")
    # print(f"sb_dict: {sb_dict}")

    for name in all_list:
        s1 = 0
        s2 = 0

        # print(f"all_list: {name}")

        if name in bm_dict:
            s1 = bm_dict[name]

        if name in sb_dict:
            s2 = sb_dict[name]

        # print(f"s1, s2: {s1, s2}")

        # print(f"find content: {k}")
        for i in range(k):
            b = bm[i]
            s = sb[i]

            # print(f"name: {name}")
            # print(f"b.meta['name']: {b.meta['name']}")
            # print(f"s.meta['name']: {s.meta['name']}")

            if b.meta["name"] == name:
                res.append({"name": name, "score": s1 + s2, "content": b.content})
                break

            else:
                if s.meta["name"] == name:
                    res.append({"name": name, "score": s1 + s2, "content": s.content})
                    break

                # else:print(f"error: {name}")

            # print("-------------")

    return sorted(res, key=lambda x: -x["score"])[:k]
