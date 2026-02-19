import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface TopicCategory {
  icon: string;
  label: string;
  count: string;
  color: string;
  colorLt: string;
}

@Component({
  selector: 'app-topics-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="topics-container">
      <div class="topics-header fade-up">
        <h1 class="serif">Housing Law <span class="highlight">Knowledge Base</span></h1>
        <p>50+ housing topics explained in plain English</p>
      </div>

      <div class="search-section fade-up" style="animation-delay: 0.1s">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" placeholder="Search housing law topics..." />
        </div>
      </div>

      <div class="categories-grid">
        <div *ngFor="let cat of categories; let i = index" 
             class="category-card fade-up"
             [style.animation-delay]="(i * 0.1 + 0.2) + 's'"
             [style.background]="cat.colorLt">
          <div class="category-icon">{{ cat.icon }}</div>
          <h3 [style.color]="cat.color">{{ cat.label }}</h3>
          <p>{{ cat.count }}</p>
        </div>
      </div>

      <div class="info-banner fade-up" style="animation-delay: 0.8s">
        <div class="banner-content">
          <h3 class="serif">Can't find what you're looking for?</h3>
          <p>Ask our AI assistant for personalized guidance on any housing law question.</p>
          <button class="btn-teal">Ask AI Assistant →</button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .topics-container {
      min-height: 100vh;
      background: var(--bg);
      padding: 60px 48px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .topics-header {
      text-align: center;
      margin-bottom: 48px;
    }

    .topics-header h1 {
      font-size: 48px;
      font-weight: 400;
      letter-spacing: -1.2px;
      color: var(--ink);
      margin-bottom: 12px;
      line-height: 1.1;
    }

    .highlight {
      color: var(--amber);
      font-style: italic;
    }

    .topics-header p {
      font-size: 18px;
      color: var(--ink3);
      font-weight: 300;
    }

    .search-section {
      margin-bottom: 48px;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }

    .search-box {
      background: #fff;
      border: 1.5px solid var(--border);
      border-radius: var(--r);
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.2s;
      box-shadow: var(--shadow-sm);
    }

    .search-box:focus-within {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0, 168, 138, 0.1);
    }

    .search-icon {
      font-size: 20px;
      opacity: 0.6;
    }

    .search-box input {
      flex: 1;
      border: none;
      outline: none;
      font-size: 15px;
      color: var(--ink);
      background: transparent;
    }

    .search-box input::placeholder {
      color: var(--ink3);
    }

    .categories-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 56px;
    }

    .category-card {
      background: #fff;
      border-radius: var(--r);
      padding: 32px 24px;
      cursor: pointer;
      transition: all 0.25s;
      border: 1px solid var(--border);
      text-align: center;
    }

    .category-card:hover {
      transform: translateY(-4px) scale(1.02);
      box-shadow: var(--shadow-md);
    }

    .category-icon {
      font-size: 40px;
      margin-bottom: 16px;
    }

    .category-card h3 {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 8px;
    }

    .category-card p {
      font-size: 13px;
      color: var(--ink3);
    }

    .info-banner {
      background: linear-gradient(135deg, var(--teal-lt), #e6f3fd);
      border: 1px solid var(--teal-mid);
      border-radius: var(--r);
      padding: 48px 40px;
      text-align: center;
    }

    .banner-content h3 {
      font-size: 28px;
      font-weight: 400;
      letter-spacing: -0.7px;
      color: var(--ink);
      margin-bottom: 12px;
    }

    .banner-content p {
      font-size: 16px;
      color: var(--ink2);
      margin-bottom: 24px;
      max-width: 500px;
      margin-left: auto;
      margin-right: auto;
    }

    @media (max-width: 768px) {
      .topics-container {
        padding: 40px 24px;
      }

      .topics-header h1 {
        font-size: 36px;
      }

      .categories-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 16px;
      }

      .info-banner {
        padding: 32px 24px;
      }
    }
  `]
})
export class TopicsListComponent {
  categories: TopicCategory[] = [
    { icon: '⚖', label: 'Eviction', count: '12 topics', color: '#d93025', colorLt: '#fdecea' },
    { icon: '🔒', label: 'Deposits', count: '8 topics', color: '#3b7dd8', colorLt: '#edf4ff' },
    { icon: '🔧', label: 'Repairs', count: '10 topics', color: '#e8840a', colorLt: '#fef3e2' },
    { icon: '📈', label: 'Rent', count: '7 topics', color: '#00a88a', colorLt: '#e6f7f4' },
    { icon: '🛡', label: 'Rights', count: '9 topics', color: '#7c6af0', colorLt: '#eeecfd' },
    { icon: '💷', label: 'Fees', count: '6 topics', color: '#22c55e', colorLt: '#f0fdf4' },
  ];
}
