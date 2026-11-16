---
layout: page
title: Chess Blogs
permalink: /chess-blogs
---

<p class="section-intro">
  Articles, stories, and thoughts on chess strategy, mindset, and history published on my 
  <a href="https://www.chess.com/blog/yasser-blog" target="_blank" rel="noopener noreferrer">
    <i class="fa fa-external-link"></i> Chess.com Blog (yasser-blog)
  </a>.
</p>

<div id="chess-gallery" class="chess-grid">
  {% for blog in site.data.chess_blogs %}
  <a href="{{ blog.url }}" class="chess-card" target="_blank" rel="noopener noreferrer" title="Read '{{ blog.title }}' on Chess.com">
    <div class="chess-card-thumb">
      <img src="{{ blog.thumbnail }}" alt="{{ blog.title }}" loading="lazy" />
      <span class="chess-badge"><i class="fa fa-bookmark"></i> Chess.com</span>
    </div>
    <div class="chess-card-body">
      <h3 class="chess-card-title">{{ blog.title }}</h3>
      <p class="chess-card-excerpt">{{ blog.excerpt }}</p>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 10px; border-top: 1px solid #f1f5f9; font-size: 0.85rem; color: #718096;">
        <span><i class="fa fa-calendar-o"></i> {{ blog.date }}</span>
        <span class="chess-card-action">
          Read on Chess.com <i class="fa fa-external-link"></i>
        </span>
      </div>
    </div>
  </a>
  {% endfor %}
</div>


<div id="chess-pagination" class="gallery-pagination" role="navigation" aria-label="Chess blog pages"></div>

<script>
(function() {
  var ITEMS_PER_PAGE = 10;
  var items = Array.prototype.slice.call(document.querySelectorAll('#chess-gallery .chess-card'));
  var totalItems = items.length;
  var totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
  var paginationContainer = document.getElementById('chess-pagination');
  var galleryContainer = document.getElementById('chess-gallery');

  if (totalPages <= 1) {
    if (paginationContainer) paginationContainer.style.display = 'none';
    return;
  }

  function getPageFromHash() {
    var match = window.location.hash.match(/page=(\d+)/);
    if (match) {
      var p = parseInt(match[1], 10);
      if (p >= 1 && p <= totalPages) return p;
    }
    return 1;
  }

  function renderPage(page, scrollToTop) {
    var start = (page - 1) * ITEMS_PER_PAGE;
    var end = start + ITEMS_PER_PAGE;

    items.forEach(function(item, idx) {
      if (idx >= start && idx < end) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });

    renderControls(page);

    if (scrollToTop && galleryContainer) {
      galleryContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function renderControls(currentPage) {
    if (!paginationContainer) return;
    paginationContainer.innerHTML = '';

    // Previous Button
    var prevBtn = document.createElement('button');
    prevBtn.className = 'gallery-page-btn' + (currentPage === 1 ? ' disabled' : '');
    prevBtn.innerHTML = '<i class="fa fa-chevron-left"></i> Previous';
    prevBtn.disabled = (currentPage === 1);
    prevBtn.onclick = function() {
      if (currentPage > 1) {
        window.location.hash = 'page=' + (currentPage - 1);
      }
    };
    paginationContainer.appendChild(prevBtn);

    // Page Numbers
    for (var i = 1; i <= totalPages; i++) {
      (function(p) {
        var numBtn = document.createElement('button');
        numBtn.className = 'gallery-page-btn' + (p === currentPage ? ' active' : '');
        numBtn.textContent = p;
        numBtn.onclick = function() {
          window.location.hash = 'page=' + p;
        };
        paginationContainer.appendChild(numBtn);
      })(i);
    }

    // Next Button
    var nextBtn = document.createElement('button');
    nextBtn.className = 'gallery-page-btn' + (currentPage === totalPages ? ' disabled' : '');
    nextBtn.innerHTML = 'Next <i class="fa fa-chevron-right"></i>';
    nextBtn.disabled = (currentPage === totalPages);
    nextBtn.onclick = function() {
      if (currentPage < totalPages) {
        window.location.hash = 'page=' + (currentPage + 1);
      }
    };
    paginationContainer.appendChild(nextBtn);

    // Page status indicator
    var status = document.createElement('span');
    status.className = 'gallery-page-status';
    status.textContent = 'Showing page ' + currentPage + ' of ' + totalPages + ' (' + totalItems + ' articles)';
    paginationContainer.appendChild(status);
  }

  window.addEventListener('hashchange', function() {
    renderPage(getPageFromHash(), true);
  });

  // Initial render
  renderPage(getPageFromHash(), false);
})();
</script>
