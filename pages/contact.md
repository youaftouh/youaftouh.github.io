---
layout: page
title: Contact
permalink: /contact
---

<p class="section-intro">
  Have a question, collaboration inquiry, or just want to say hello? Send me a message using the form below and it will be delivered directly to my inbox at <strong>yasser.ouaftouh@gmail.com</strong>.
</p>

<div class="contact-wrapper">
  <div class="contact-card">
    <form action="https://formsubmit.co/yasser.ouaftouh@gmail.com" method="POST">
      <!-- Anti-spam Honeypot -->
      <input type="text" name="_honey" style="display:none">

      <!-- Form Configuration -->
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="https://youaftouh.github.io/contact?submitted=true">

      <div class="contact-form-group">
        <label for="contact-name"><i class="fa fa-user"></i> Your Name</label>
        <input type="text" id="contact-name" name="name" placeholder="John Doe" required>
      </div>

      <div class="contact-form-group">
        <label for="contact-email"><i class="fa fa-envelope-o"></i> Your Email Address</label>
        <input type="email" id="contact-email" name="email" placeholder="john.doe@example.com" required>
      </div>

      <div class="contact-form-group">
        <label for="contact-subject"><i class="fa fa-tag"></i> Subject</label>
        <input type="text" id="contact-subject" name="_subject" placeholder="Project collaboration / Inquiry" required>
      </div>

      <div class="contact-form-group">
        <label for="contact-message"><i class="fa fa-commenting-o"></i> Message</label>
        <textarea id="contact-message" name="message" rows="6" placeholder="Write your message here..." required></textarea>
      </div>

      <button type="submit" class="contact-submit-btn">
        <i class="fa fa-paper-plane"></i> Send Message
      </button>

      <div class="contact-security-notice">
        <i class="fa fa-shield"></i> Messages are transmitted securely via encrypted SSL.
      </div>
    </form>
  </div>

  <div class="contact-social-options">
    <h3><i class="fa fa-share-alt"></i> Other Ways to Connect</h3>
    <p style="margin-top: 4px; color: #64748b; font-size: 0.92rem;">
      You can also reach out to me via my social channels or GitHub:
    </p>

    <div class="contact-options-grid">
      <a href="https://twitter.com/intent/tweet?text=Hi%20@youaftouh%20" target="_blank" rel="noopener noreferrer" class="contact-option-card">
        <i class="fa fa-twitter" style="color: #00aced;"></i>
        <span>Tweet at Me</span>
      </a>

      <a href="https://github.com/youaftouh/youaftouh.github.io/issues/new" target="_blank" rel="noopener noreferrer" class="contact-option-card">
        <i class="fa fa-github" style="color: #333333;"></i>
        <span>File a GitHub Issue</span>
      </a>

      <a href="https://www.linkedin.com/in/youaftouh/" target="_blank" rel="noopener noreferrer" class="contact-option-card">
        <i class="fa fa-linkedin" style="color: #0073a4;"></i>
        <span>Connect on LinkedIn</span>
      </a>

      <a href="mailto:yasser.ouaftouh@gmail.com" class="contact-option-card">
        <i class="fa fa-envelope" style="color: #f39c12;"></i>
        <span>Direct Gmail</span>
      </a>
    </div>
  </div>
</div>
