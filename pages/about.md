---
layout: page
title: About Me
permalink: /about
---

<div class="about-hero">
  <div class="about-avatar-wrap">
    <img src="https://media.licdn.com/dms/image/v2/C4D03AQGWdFKBHxZFbw/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1557919212179?e=2147483647&amp;v=beta&amp;t=YQ4fICigAQN6FP13OtThOgPBqQY3s8kMuQfnLrTfS-M" alt="Yasser Ouaftouh" />
  </div>
  <div class="about-hero-text">
    <h2>Hi, I'm Yasser Ouaftouh.</h2>
    <p class="about-hero-tagline">
      Software engineer specializing in SAP Commerce, Java, and enterprise software development.
    </p>
  </div>
</div>

<p>I'm a software engineer based in Dublin, Ireland, specializing in SAP Commerce (formerly Hybris). My background spans enterprise software development, Java, Spring, and related technologies, with experience building digital commerce platforms and distributed applications.</p>

<h2>Education</h2>
<p>École Nationale des Sciences Appliquées d'Oujda (ENSAO), Morocco · 2009–2014</p>

<h2>Certifications &amp; recognition</h2>
<ul>
  <li>Top Scorer — Deloitte SAP Challenge Europe, 2024</li>
  <li>AWS Certified Developer – Associate, 2024</li>
  <li>AWS Certified Cloud Practitioner, 2024</li>
  <li>Professional Scrum Master I, 2020</li>
  <li>SAP Hybris Commerce V5, 2015</li>
  <li>SAP Hybris Core Platform V5, 2015</li>
</ul>

<h2 id="projects">Selected projects</h2>
<div class="about-highlights-grid">
  {% for project in site.data.projects %}
  <div class="about-highlight-card">
    <h3>{{ project.name | escape }}</h3>
    <p>{{ project.description | escape }}</p>
    <p class="project-technologies">{{ project.technologies | escape }}</p>
  </div>
  {% endfor %}
</div>

<h2>Hackathons &amp; experiments</h2>
<p>I also explore ideas through hackathons, AI-assisted development, and small games.</p>
<div class="about-highlights-grid">
  <div class="about-highlight-card">
    <h3><a href="https://devpost.com/software/tree-planting-tracker-0pau3o" target="_blank" rel="noopener noreferrer">Tree Planting Tracker ↗</a></h3>
    <p>February 2026 · Hack for Humanity</p>
    <p>A community application for logging tree planting, with interactive maps, CO₂ estimates, heatmaps, leaderboards, and AI-based species recommendations.</p>
    <p class="project-technologies">React · TypeScript · Firebase · Leaflet · Vercel</p>
  </div>
  <div class="about-highlight-card">
    <h3><a href="https://devpost.com/software/lia-s-escape" target="_blank" rel="noopener noreferrer">Lia's Escape ↗</a></h3>
    <p>May 2026 · Maki 2D Pixel RPG Game</p>
    <p>An experimental 2D escape-room game about finding a way from a room to a garden, created with AI-assisted game-development tools.</p>
  </div>
  <div class="about-highlight-card">
    <h3><a href="https://devpost.com/software/shutdowntimer-resurrection" target="_blank" rel="noopener noreferrer">ShutdownTimer [Resurrection] ↗</a></h3>
    <p>December 2025 · Kiroween</p>
    <p>A macOS recreation of an application I originally developed as a teenager, rebuilt with Kiro AI-assisted development.</p>
  </div>
</div>

<h2>Activities &amp; hobbies</h2>
<p>Outside work, I enjoy programming challenges on CodinGame, experimenting with new tools, games, chess, and drone photography. I share some of these interests through <a href="{{ '/chess-blogs' | relative_url }}">chess articles</a> and <a href="{{ '/drone-videos' | relative_url }}">drone videos on EireFly</a>.</p>

<h3>Where to find me</h3>
<p>For professional conversations, project ideas, or shared interests, feel free to connect.</p>

<div class="about-connect-banner">
  <div class="about-connect-links">
    <a href="https://www.linkedin.com/in/youaftouh/" target="_blank" rel="noopener noreferrer" class="about-social-pill">
      <i class="fa fa-linkedin"></i> LinkedIn
    </a>
    <a href="https://github.com/youaftouh" target="_blank" rel="noopener noreferrer" class="about-social-pill">
      <i class="fa fa-github"></i> GitHub
    </a>
    <a href="https://www.youtube.com/@eirefly/videos" target="_blank" rel="noopener noreferrer" class="about-social-pill">
      <i class="fa fa-youtube-play"></i> YouTube (@eirefly)
    </a>
    <a href="https://www.chess.com/blog/yasser-blog" target="_blank" rel="noopener noreferrer" class="about-social-pill">
      <i class="fa fa-pencil-square-o"></i> Chess.com Blog
    </a>
    <a href="https://twitter.com/youaftouh" target="_blank" rel="noopener noreferrer" class="about-social-pill">
      <i class="fa fa-twitter"></i> Twitter / X
    </a>
    <a href="mailto:yasser.ouaftouh@gmail.com" class="about-social-pill">
      <i class="fa fa-envelope"></i> Email Me
    </a>
  </div>
</div>
