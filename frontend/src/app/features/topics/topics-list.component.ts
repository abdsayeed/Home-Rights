import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { TopicsService } from '../../core/services/topics.service';

interface TopicCategory {
  icon: string;
  label: string;
  value: string;
  count: string;
  color: string;
  colorLt: string;
}

@Component({
  selector: 'app-topics-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="topics-container">
      <div class="topics-header fade-up">
        <h1 class="serif">Housing Law <span class="highlight">Knowledge Base</span></h1>
        <p>{{ totalTopics() }} housing topics explained in plain English</p>
      </div>

      <div class="search-section fade-up" style="animation-delay: 0.1s">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            placeholder="Search housing law topics..." 
            [(ngModel)]="searchTerm"
            (input)="onSearch()" />
        </div>
        
        <div class="filters">
          <select [(ngModel)]="selectedCategory" (change)="onFilterChange()" class="filter-select">
            <option value="">All Categories</option>
            <option *ngFor="let cat of categories" [value]="cat.value">{{ cat.label }}</option>
          </select>
          
          <select [(ngModel)]="sortBy" (change)="onSortChange()" class="filter-select">
            <option value="title">Alphabetical</option>
            <option value="views">Most Viewed</option>
            <option value="date">Recently Added</option>
          </select>
        </div>
      </div>

      @if (loading()) {
        <div class="loading">Loading topics...</div>
      } @else if (topics().length === 0) {
        <div class="no-results">
          <p>No topics found matching your search.</p>
        </div>
      } @else {
        <div class="topics-list">
          @for (topic of topics(); track topic.id) {
            <div class="topic-card fade-up" [routerLink]="['/topics', topic.slug]">
              <div class="topic-header">
                <span class="topic-category" [style.background]="getCategoryColor(topic.category)">
                  {{ getCategoryLabel(topic.category) }}
                </span>
              </div>
              <h3>{{ topic.title }}</h3>
              <p>{{ topic.summary }}</p>
              <div class="topic-meta">
                <span class="meta-item">📚 {{ topic.category }}</span>
                @if (topic.lastUpdated) {
                  <span class="meta-item">🕒 Updated {{ formatDate(topic.lastUpdated) }}</span>
                }
                @if (topic.difficulty) {
                  <span class="meta-item">📊 {{ topic.difficulty }}</span>
                }
              </div>
              <div class="topic-tags">
                <span *ngFor="let tag of topic.tags" class="tag">{{ tag }}</span>
              </div>
            </div>
          }
        </div>

        <div class="pagination" *ngIf="totalPages() > 1">
          <button 
            [disabled]="currentPage() === 1" 
            (click)="goToPage(currentPage() - 1)"
            class="btn-pagination">
            ← Previous
          </button>
          <span class="page-info">Page {{ currentPage() }} of {{ totalPages() }}</span>
          <button 
            [disabled]="currentPage() === totalPages()" 
            (click)="goToPage(currentPage() + 1)"
            class="btn-pagination">
            Next →
          </button>
        </div>
      }

      <div class="info-banner fade-up" style="animation-delay: 0.8s">
        <div class="banner-content">
          <h3 class="serif">Can't find what you're looking for?</h3>
          <p>Ask our AI assistant for personalized guidance on any housing law question.</p>
          <button class="btn-teal" routerLink="/chat">Ask AI Assistant →</button>
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
      max-width: 800px;
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
      margin-bottom: 16px;
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

    .filters {
      display: flex;
      gap: 12px;
      justify-content: center;
    }

    .filter-select {
      padding: 10px 16px;
      border: 1.5px solid var(--border);
      border-radius: var(--r);
      background: white;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .filter-select:hover {
      border-color: var(--teal);
    }

    .topics-list {
      display: grid;
      gap: 20px;
      margin-bottom: 40px;
    }

    .topic-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 24px;
      cursor: pointer;
      transition: all 0.25s;
    }

    .topic-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--teal);
    }

    .topic-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .topic-category {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      color: white;
    }

    .topic-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 12px;
      font-size: 13px;
      color: var(--ink3);
    }

    .meta-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .topic-card h3 {
      font-size: 20px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 8px;
    }

    .topic-card p {
      font-size: 15px;
      color: var(--ink2);
      line-height: 1.6;
      margin-bottom: 12px;
    }

    .topic-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .tag {
      padding: 4px 10px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      font-size: 12px;
      color: var(--ink2);
    }

    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      margin-bottom: 40px;
    }

    .btn-pagination {
      padding: 10px 20px;
      border: 1.5px solid var(--border);
      background: white;
      border-radius: var(--r);
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s;
    }

    .btn-pagination:hover:not(:disabled) {
      background: var(--teal);
      color: white;
      border-color: var(--teal);
    }

    .btn-pagination:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    .page-info {
      font-size: 14px;
      color: var(--ink2);
    }

    .loading, .no-results {
      text-align: center;
      padding: 60px 20px;
      color: var(--ink3);
      font-size: 16px;
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

      .filters {
        flex-direction: column;
      }

      .filter-select {
        width: 100%;
      }
    }
  `]
})
export class TopicsListComponent implements OnInit {
  topics = signal<any[]>([]);
  loading = signal(true);
  currentPage = signal(1);
  totalPages = signal(1);
  totalTopics = signal(0);
  searchTerm = '';
  selectedCategory = '';
  sortBy = 'title';

  categories: TopicCategory[] = [
    { icon: '⚖', label: 'Eviction', value: 'eviction', count: '12 topics', color: '#d93025', colorLt: '#fdecea' },
    { icon: '🔒', label: 'Deposits', value: 'deposits', count: '8 topics', color: '#3b7dd8', colorLt: '#edf4ff' },
    { icon: '🔧', label: 'Repairs', value: 'repairs', count: '10 topics', color: '#e8840a', colorLt: '#fef3e2' },
    { icon: '📈', label: 'Rent', value: 'rent', count: '7 topics', color: '#00a88a', colorLt: '#e6f7f4' },
    { icon: '🛡', label: 'Rights', value: 'rights', count: '9 topics', color: '#7c6af0', colorLt: '#eeecfd' },
    { icon: '💷', label: 'Fees', value: 'fees', count: '6 topics', color: '#22c55e', colorLt: '#f0fdf4' },
  ];

  constructor(private topicsService: TopicsService) {}

  ngOnInit() {
    this.loadTopics();
  }

  loadTopics() {
    this.loading.set(true);
    
    const params: any = {
      page: this.currentPage(),
      limit: 20,
      sort: this.sortBy
    };
    
    if (this.searchTerm) params.search = this.searchTerm;
    if (this.selectedCategory) params.category = this.selectedCategory;
    
    this.topicsService.getTopics(
      this.selectedCategory, 
      this.searchTerm
    ).subscribe({
      next: (response: any) => {
        this.topics.set(response.topics || []);
        if (response.pagination) {
          this.totalPages.set(response.pagination.totalPages);
          this.totalTopics.set(response.pagination.total);
        }
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Failed to load topics:', error);
        this.loading.set(false);
      }
    });
  }

  onSearch() {
    this.currentPage.set(1);
    this.loadTopics();
  }

  onFilterChange() {
    this.currentPage.set(1);
    this.loadTopics();
  }

  onSortChange() {
    this.currentPage.set(1);
    this.loadTopics();
  }

  goToPage(page: number) {
    this.currentPage.set(page);
    this.loadTopics();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  getCategoryLabel(value: string): string {
    const cat = this.categories.find(c => c.value === value);
    return cat ? cat.label : value;
  }

  getCategoryColor(value: string): string {
    const cat = this.categories.find(c => c.value === value);
    return cat ? cat.color : '#666';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'today';
    if (diffDays === 1) return 'yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return date.toLocaleDateString();
  }
}
