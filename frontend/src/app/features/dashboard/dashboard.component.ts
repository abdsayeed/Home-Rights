import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="dashboard-container">
      <div class="dashboard-header fade-up">
        <h1 class="serif">Welcome to <span class="highlight">HomeRights AI</span></h1>
        <p>Your AI-powered housing rights assistant</p>
      </div>

      <div class="features-grid">
        <a routerLink="/documents" class="feature-card fade-up" style="animation-delay: 0.1s">
          <div class="feature-icon" style="background: var(--teal-lt); border: 1px solid var(--teal-mid)">
            <span style="font-size: 32px">◰</span>
          </div>
          <h3 class="serif">Document Analysis</h3>
          <p>Upload any tenancy document and get an instant risk report with ML-powered classification.</p>
          <div class="feature-meta">
            <span class="pill pill-teal">PDF, JPG, PNG</span>
          </div>
        </a>

        <a routerLink="/chat" class="feature-card fade-up" style="animation-delay: 0.2s">
          <div class="feature-icon" style="background: var(--purple-lt); border: 1px solid #d4c5f9">
            <span style="font-size: 32px">◎</span>
          </div>
          <h3 class="serif">AI Legal Assistant</h3>
          <p>Ask any housing question and get clear, UK-law-grounded answers with relevant legislation.</p>
          <div class="feature-meta">
            <span class="pill" style="background: var(--purple-lt); color: var(--purple)">24/7 Available</span>
          </div>
        </a>

        <a routerLink="/topics" class="feature-card fade-up" style="animation-delay: 0.3s">
          <div class="feature-icon" style="background: var(--amber-lt); border: 1px solid #f5c98f">
            <span style="font-size: 32px">◫</span>
          </div>
          <h3 class="serif">Law Knowledge Base</h3>
          <p>50+ housing topics explained in plain English across 8 categories with legal references.</p>
          <div class="feature-meta">
            <span class="pill pill-amber">50+ Topics</span>
          </div>
        </a>

        <a routerLink="/support" class="feature-card fade-up" style="animation-delay: 0.4s">
          <div class="feature-icon" style="background: var(--red-lt); border: 1px solid #f5b5b0">
            <span style="font-size: 32px">◉</span>
          </div>
          <h3 class="serif">Support Finder</h3>
          <p>Find housing charities and legal aid near you with location and issue-type filtering.</p>
          <div class="feature-meta">
            <span class="pill pill-red">100+ Organisations</span>
          </div>
        </a>
      </div>

      <div class="info-section fade-up" style="animation-delay: 0.5s">
        <div class="info-card">
          <h3 class="serif">How it works</h3>
          <div class="steps">
            <div class="step">
              <span class="step-number">01</span>
              <div>
                <h4>Upload your document</h4>
                <p>Drag & drop your tenancy agreement or housing document</p>
              </div>
            </div>
            <div class="step">
              <span class="step-number">02</span>
              <div>
                <h4>AI analyses for risks</h4>
                <p>ML pipeline detects legal issues with severity ratings</p>
              </div>
            </div>
            <div class="step">
              <span class="step-number">03</span>
              <div>
                <h4>Ask follow-up questions</h4>
                <p>Get answers in plain English with legal citations</p>
              </div>
            </div>
            <div class="step">
              <span class="step-number">04</span>
              <div>
                <h4>Find local support</h4>
                <p>Connect with Shelter, Citizens Advice, and legal aid</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      min-height: 100vh;
      background: var(--bg);
      padding: 60px 48px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .dashboard-header {
      text-align: center;
      margin-bottom: 56px;
    }

    .dashboard-header h1 {
      font-size: 48px;
      font-weight: 400;
      letter-spacing: -1.2px;
      color: var(--ink);
      margin-bottom: 12px;
      line-height: 1.1;
    }

    .highlight {
      color: var(--teal);
      font-style: italic;
    }

    .dashboard-header p {
      font-size: 18px;
      color: var(--ink3);
      font-weight: 300;
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 24px;
      margin-bottom: 48px;
    }

    .feature-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 32px 28px;
      transition: all 0.25s;
      cursor: pointer;
      text-decoration: none;
      color: inherit;
      display: flex;
      flex-direction: column;
    }

    .feature-card:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-4px);
    }

    .feature-icon {
      width: 64px;
      height: 64px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 20px;
    }

    .feature-card h3 {
      font-size: 22px;
      font-weight: 400;
      letter-spacing: -0.5px;
      color: var(--ink);
      margin-bottom: 12px;
    }

    .feature-card p {
      font-size: 14px;
      color: var(--ink3);
      line-height: 1.65;
      margin-bottom: 16px;
      flex: 1;
    }

    .feature-meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .info-section {
      margin-top: 48px;
    }

    .info-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 40px;
      box-shadow: var(--shadow-sm);
    }

    .info-card h3 {
      font-size: 32px;
      font-weight: 400;
      letter-spacing: -0.8px;
      color: var(--ink);
      margin-bottom: 32px;
      text-align: center;
    }

    .steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 32px;
    }

    .step {
      display: flex;
      gap: 16px;
    }

    .step-number {
      font-family: 'Courier New', monospace;
      font-size: 11px;
      color: var(--teal);
      letter-spacing: 1px;
      font-weight: 600;
      flex-shrink: 0;
    }

    .step h4 {
      font-size: 16px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 6px;
    }

    .step p {
      font-size: 13px;
      color: var(--ink3);
      line-height: 1.6;
    }

    @media (max-width: 768px) {
      .dashboard-container {
        padding: 40px 24px;
      }

      .dashboard-header h1 {
        font-size: 36px;
      }

      .features-grid {
        grid-template-columns: 1fr;
      }

      .steps {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class DashboardComponent {}
