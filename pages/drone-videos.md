---
layout: page
title: Drone Videos
permalink: /drone-videos
---

<div class="drone-channel-banner">
  <div class="drone-channel-info">
    <i class="fa fa-youtube-play drone-channel-icon" aria-hidden="true"></i>
    <div>
      <h3 style="margin: 0; font-size: 1.25rem;">EireFly Aerial Cinematography</h3>
      <p style="margin: 4px 0 0; color: #64748b; font-size: 0.92rem;">
        Exploring scenic landscapes, coastal cliffs, and mountain peaks across Ireland and beyond from above. Click any video to watch in-page!
      </p>
    </div>
  </div>
  <a href="https://www.youtube.com/@eirefly/videos" target="_blank" rel="noopener noreferrer" class="drone-btn-subscribe">
    <i class="fa fa-youtube"></i> Visit Channel
  </a>
</div>

<div id="drone-gallery" class="drone-gallery-grid">
  {% for video in site.data.drone_videos %}
  <div class="drone-gallery-item" data-index="{{ forloop.index0 }}">
    <div class="drone-card drone-play-btn" data-video-id="{{ video.id }}" data-video-title="{{ video.title }}" data-video-url="{{ video.youtube_url }}" title="Play '{{ video.title }}' in-page">
      <div class="drone-thumb-container">
        <img src="{{ video.thumbnail }}" alt="{{ video.title }}" loading="lazy" />
        <div class="drone-play-overlay">
          <i class="fa fa-play" style="margin-left: 3px;"></i>
        </div>
      </div>
      <div class="drone-card-info">
        <h4 class="drone-card-title">{{ video.title }}</h4>
        <div class="drone-card-meta">
          <span class="drone-card-location">
            <i class="fa fa-map-marker"></i> {{ video.location }}
          </span>
          <span class="drone-card-action">
            <i class="fa fa-play-circle"></i> Watch Video
          </span>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<!-- Paginated Gallery Controls (9 items per page) -->
<div id="drone-pagination" class="gallery-pagination"></div>

<!-- In-Page YouTube Video Modal -->
<div id="video-modal" class="video-modal" style="display: none;" role="dialog" aria-modal="true" aria-hidden="true">
  <div class="video-modal-backdrop" id="video-modal-backdrop"></div>
  <div class="video-modal-dialog">
    <div class="video-modal-header">
      <h3 id="video-modal-title" class="video-modal-title">Watch Video</h3>
      <button type="button" id="video-modal-close" class="video-modal-close" aria-label="Close video">&times;</button>
    </div>
    <div class="video-modal-body">
      <div class="video-modal-responsive">
        <iframe id="video-modal-iframe" src="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
      </div>
    </div>
    <div class="video-modal-footer">
      <span class="video-modal-tip"><i class="fa fa-info-circle"></i> Press ESC or click outside to close</span>
      <a id="video-modal-yt-link" href="" target="_blank" rel="noopener noreferrer" class="video-modal-yt-btn">
        <i class="fa fa-youtube-play"></i> Open on YouTube ↗
      </a>
    </div>
  </div>
</div>

<script>
(function() {
  /* ==========================================================================
     In-Page Video Modal Functionality
     ========================================================================== */
  var modal = document.getElementById('video-modal');
  var modalBackdrop = document.getElementById('video-modal-backdrop');
  var modalClose = document.getElementById('video-modal-close');
  var modalIframe = document.getElementById('video-modal-iframe');
  var modalTitle = document.getElementById('video-modal-title');
  var modalYtLink = document.getElementById('video-modal-yt-link');

  function openVideoModal(videoId, title, ytUrl) {
    if (!modal) return;
    modalTitle.textContent = title || 'Watch Video';
    modalYtLink.href = ytUrl || ('https://www.youtube.com/watch?v=' + videoId);
    modalIframe.src = 'https://www.youtube-nocookie.com/embed/' + videoId + '?autoplay=1&rel=0&modestbranding=1';
    modal.style.display = 'flex';
    // Force reflow for CSS transition
    modal.offsetHeight;
    modal.classList.add('is-active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeVideoModal() {
    if (!modal) return;
    modal.classList.remove('is-active');
    modal.setAttribute('aria-hidden', 'true');
    modalIframe.src = '';
    document.body.style.overflow = '';
    setTimeout(function() {
      if (!modal.classList.contains('is-active')) {
        modal.style.display = 'none';
      }
    }, 250);
  }

  if (modalBackdrop) modalBackdrop.addEventListener('click', closeVideoModal);
  if (modalClose) modalClose.addEventListener('click', closeVideoModal);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' || e.keyCode === 27) {
      if (modal && modal.classList.contains('is-active')) {
        closeVideoModal();
      }
    }
  });

  // Attach click listener to all video cards
  var playButtons = document.querySelectorAll('.drone-play-btn');
  for (var i = 0; i < playButtons.length; i++) {
    playButtons[i].addEventListener('click', function(e) {
      e.preventDefault();
      var vidId = this.getAttribute('data-video-id');
      var title = this.getAttribute('data-video-title');
      var ytUrl = this.getAttribute('data-video-url');
      if (vidId) {
        openVideoModal(vidId, title, ytUrl);
      }
    });
  }

  /* ==========================================================================
     Paginated Gallery Logic (9 items per page)
     ========================================================================== */
  var ITEMS_PER_PAGE = 9;
  var items = Array.prototype.slice.call(document.querySelectorAll('.drone-gallery-item'));
  var totalItems = items.length;
  var totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
  var paginationContainer = document.getElementById('drone-pagination');
  var galleryContainer = document.getElementById('drone-gallery');

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
    status.textContent = 'Showing page ' + currentPage + ' of ' + totalPages + ' (' + totalItems + ' videos)';
    paginationContainer.appendChild(status);
  }

  window.addEventListener('hashchange', function() {
    renderPage(getPageFromHash(), true);
  });

  // Initial render
  renderPage(getPageFromHash(), false);
})();
</script>
