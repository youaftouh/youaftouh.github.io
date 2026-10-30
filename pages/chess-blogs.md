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

<div class="chess-grid">
  {% for blog in site.data.chess_blogs %}
  <a href="{{ blog.url }}" class="chess-card" target="_blank" rel="noopener noreferrer" title="Read '{{ blog.title }}' on Chess.com">
    <div class="chess-card-thumb">
      <img src="{{ blog.thumbnail }}" alt="{{ blog.title }}" loading="lazy" />
      <span class="chess-badge"><i class="fa fa-bookmark"></i> Chess.com</span>
    </div>
    <div class="chess-card-body">
      <h3 class="chess-card-title">{{ blog.title }}</h3>
      <p class="chess-card-excerpt">{{ blog.excerpt }}</p>
      <div class="chess-card-action">
        Read on Chess.com <i class="fa fa-external-link"></i>
      </div>
    </div>
  </a>
  {% endfor %}
</div>
