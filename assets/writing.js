(() => {
  const form = document.querySelector('.writing-filters');
  if (!form) return;
  const keyword = document.getElementById('keyword');
  const tag = document.getElementById('tag-filter');
  const count = document.getElementById('result-count');
  const empty = document.getElementById('no-results');
  const articles = [...document.querySelectorAll('#writing-list .post')].map(element => ({
    element,
    text: element.dataset.search.toLocaleLowerCase(),
    tags: JSON.parse(element.dataset.tags)
  }));
  function filter() {
    const words = keyword.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const article of articles) {
      const matches = words.every(word => article.text.includes(word)) && (!tag.value || article.tags.includes(tag.value));
      article.element.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = `${visible} of ${articles.length} article${articles.length === 1 ? '' : 's'}`;
    empty.hidden = visible !== 0;
  }
  form.hidden = false;
  count.hidden = false;
  form.addEventListener('submit', event => event.preventDefault());
  keyword.addEventListener('input', filter);
  tag.addEventListener('change', filter);
  form.addEventListener('reset', () => {
    keyword.value = '';
    tag.value = '';
    filter();
  });
  filter();
})();
