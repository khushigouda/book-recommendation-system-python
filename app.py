from flask import Flask,render_template,request
import pickle
import numpy as np
import re, unicodedata
try:
    from rapidfuzz import process, fuzz
    HAVE_RAPIDFUZZ = True
except ImportError:
    import difflib
    HAVE_RAPIDFUZZ = False

k = 5
threshold = 80


popular_df= pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)
app = Flask(__name__, static_folder="model/static")


def _nz(s: str) -> str:
    s = s.lower().strip()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", s)

# Build initial mapping of normalized keys to titles from pt.index (your pivot table index)
norm_key_to_title = {}
for t in pt.index:
    t_str = str(t)
    norm_key = _nz(t_str)
    if norm_key not in norm_key_to_title:
        norm_key_to_title[norm_key] = t_str
norm_keys = list(norm_key_to_title.keys())


def resolve_title_in_pivot_v4(user_query: str, threshold: int = 80, n_suggestions: int = 5):
    qn = _nz(user_query)

    if qn in norm_key_to_title:
        return norm_key_to_title[qn], 100, []

    suggestions = []
    if HAVE_RAPIDFUZZ:
        best = process.extractOne(qn, norm_keys, scorer=fuzz.ratio)
        topk = process.extract(qn, norm_keys, scorer=fuzz.ratio, limit=n_suggestions)
        suggestions = [(norm_key_to_title[k], int(score)) for (k, score, _) in topk]
        if best and best[1] >= threshold:
            return norm_key_to_title[best[0]], int(best[1]), suggestions
    else:
        matches = difflib.get_close_matches(qn, norm_keys, n_suggestions, cutoff=threshold/100)
        suggestions = [(norm_key_to_title[k], int(100*difflib.SequenceMatcher(None, qn, k).ratio())) for k in matches]
        if matches:
            best_key = matches[0]
            best_score = int(100*difflib.SequenceMatcher(None, qn, best_key).ratio())
            if best_score >= threshold:
                return norm_key_to_title[best_key], best_score, suggestions

    return None, 0, suggestions


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    resolved, score, sugg = resolve_title_in_pivot_v4(user_input, threshold=threshold)
    if not resolved:
        return render_template('recommend.html', data=[], user_input=user_input, suggestions=sugg)
    if resolved not in pt.index:
        # (normalization code as you have)
        if resolved not in pt.index:
            return render_template('recommend.html', data=[], user_input=user_input, suggestions=sugg)
    idx = pt.index.get_loc(resolved)
    similar_items = sorted(
        list(enumerate(similarity_scores[idx])),
        key=lambda x: x[1],
        reverse=True
    )[1:k + 1]
    results = [pt.index[i] for i, _ in similar_items]

    data = []
    for title in results:
        temp_df = books[books['Book-Title'] == title]
        temp_df = temp_df.drop_duplicates('Book-Title')
        item = [
            list(temp_df['Book-Title'].values),
            list(temp_df['Book-Author'].values),
            list(temp_df['Image-URL-M'].values)
        ]
        data.append(item)
    return render_template('recommend.html', data=data, user_input=user_input, suggestions=[])


if __name__ == '__main__':
    app.run(debug=True)
