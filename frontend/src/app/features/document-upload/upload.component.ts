import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DocumentService, DocumentAnalysis } from '../../core/services/document.service';



@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="upload-container">
      <div class="upload-card">
        <h1>📄 Document Analysis</h1>
        <p class="subtitle">Upload your housing document for instant AI analysis</p>

        <!-- Upload Area -->
        <div class="upload-area" 
             [class.dragover]="isDragging()"
             (dragover)="onDragOver($event)"
             (dragleave)="onDragLeave($event)"
             (drop)="onDrop($event)"
             *ngIf="!isAnalyzing() && !result()">
          <input 
            type="file" 
            #fileInput 
            (change)="onFileSelected($event)"
            accept=".pdf,.jpg,.jpeg,.png"
            style="display: none"
          />
          
          <div class="upload-icon">📁</div>
          <h3>Drop your document here</h3>
          <p>or</p>
          <button (click)="fileInput.click()" class="upload-btn">
            Choose File
          </button>
          <p class="file-types">Supported: PDF, JPG, PNG (Max 10MB)</p>
        </div>

        <!-- Processing -->
        <div class="processing" *ngIf="isAnalyzing()">
          <div class="spinner"></div>
          <h3>Analyzing Document...</h3>
          <p>{{ processingStatus() }}</p>
        </div>

        <!-- Results -->
        <div class="results" *ngIf="result() && !isAnalyzing()">
          <!-- Header -->
          <div class="results-header">
            <h2>Analysis Complete</h2>
            <button (click)="reset()" class="btn-secondary">
              Analyze Another Document
            </button>
          </div>

          <!-- Classification -->
          <div class="result-card">
            <h3>📋 Document Type</h3>
            <div class="classification">
              <span class="category">{{ formatCategory(result()!.classification.category) }}</span>
              <span class="confidence">{{ (result()!.classification.confidence * 100).toFixed(1) }}% confidence</span>
            </div>
          </div>

          <!-- Risk Assessment -->
          <div class="result-card" [class]="'risk-' + result()!.severity_analysis.overall_risk.toLowerCase()">
            <h3>⚠️ Risk Assessment</h3>
            <div class="risk-level">
              <span class="risk-badge">{{ result()!.severity_analysis.overall_risk }}</span>
            </div>
            <div class="issue-counts">
              <span *ngIf="result()!.severity_analysis.critical_count > 0" class="count critical">
                {{ result()!.severity_analysis.critical_count }} Critical
              </span>
              <span *ngIf="result()!.severity_analysis.high_count > 0" class="count high">
                {{ result()!.severity_analysis.high_count }} High
              </span>
              <span *ngIf="result()!.severity_analysis.medium_count > 0" class="count medium">
                {{ result()!.severity_analysis.medium_count }} Medium
              </span>
            </div>
          </div>

          <!-- Summary -->
          <div class="result-card">
            <h3>📝 Summary</h3>
            <p class="summary">{{ result()!.summary }}</p>
          </div>

          <!-- Issues -->
          <div class="result-card" *ngIf="result()!.detected_issues.length > 0">
            <h3>🚨 Issues Detected</h3>
            <div class="issues-list">
              <div class="issue" *ngFor="let issue of result()!.detected_issues" 
                   [class]="'severity-' + issue.severity.toLowerCase()">
                <div class="issue-header">
                  <span class="issue-title">{{ formatIssue(issue.issue) }}</span>
                  <span class="severity-badge">{{ issue.severity }}</span>
                </div>
                <p class="issue-text">"{{ issue.matched_text }}"</p>
                <p class="issue-explanation">{{ issue.explanation }}</p>
                <div class="issue-recommendations" *ngIf="issue.recommendations.length > 0">
                  <strong>What to do:</strong>
                  <ul>
                    <li *ngFor="let rec of issue.recommendations">{{ rec }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- Recommendations -->
          <div class="result-card recommendations">
            <h3>💡 Recommendations</h3>
            <ul>
              <li *ngFor="let rec of result()!.recommendations">{{ rec }}</li>
            </ul>
          </div>

          <!-- Extracted Text -->
          <div class="result-card collapsible">
            <h3 (click)="toggleText()">
              📄 Extracted Text 
              <span class="toggle">{{ showText() ? '▼' : '▶' }}</span>
            </h3>
            <div class="extracted-text" *ngIf="showText()">
              <pre>{{ result()!.extracted_text }}</pre>
            </div>
          </div>
        </div>

        <!-- Error -->
        <div class="error-message" *ngIf="error()">
          <span class="material-icons">error</span>
          <p>{{ error() }}</p>
          <button (click)="reset()">Try Again</button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .upload-container {
      min-height: 100vh;
      background: var(--bg);
      padding: 60px 48px;
    }

    .upload-card {
      max-width: 900px;
      margin: 0 auto;
      background: #fff;
      border-radius: var(--r);
      padding: 48px;
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border);
    }

    h1 {
      font-family: 'Instrument Serif', serif;
      font-size: 40px;
      font-weight: 400;
      letter-spacing: -1px;
      margin-bottom: 12px;
      color: var(--ink);
    }

    .subtitle {
      color: var(--ink3);
      font-size: 16px;
      margin-bottom: 40px;
    }

    .upload-area {
      border: 2px dashed var(--border);
      border-radius: var(--r);
      padding: 80px 40px;
      text-align: center;
      transition: all 0.3s;
      cursor: pointer;
      background: var(--bg2);
    }

    .upload-area:hover, .upload-area.dragover {
      border-color: var(--teal);
      background: var(--teal-lt);
    }

    .upload-icon {
      font-size: 72px;
      margin-bottom: 20px;
      opacity: 0.7;
    }

    .upload-area h3 {
      font-family: 'Instrument Serif', serif;
      font-size: 24px;
      font-weight: 400;
      color: var(--ink);
      margin-bottom: 8px;
    }

    .upload-area p {
      color: var(--ink3);
      margin: 8px 0;
    }

    .upload-btn {
      background: var(--teal);
      color: white;
      border: none;
      padding: 14px 32px;
      border-radius: var(--r-full);
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      margin: 20px 0;
      box-shadow: 0 2px 12px rgba(0, 168, 138, 0.28);
      transition: all 0.2s;
    }

    .upload-btn:hover {
      background: #009a7e;
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(0, 168, 138, 0.35);
    }

    .file-types {
      color: var(--ink4);
      font-size: 13px;
      margin-top: 16px;
    }

    .processing {
      text-align: center;
      padding: 80px 40px;
    }

    .processing h3 {
      font-family: 'Instrument Serif', serif;
      font-size: 24px;
      font-weight: 400;
      color: var(--ink);
      margin-bottom: 12px;
    }

    .processing p {
      color: var(--ink3);
      font-size: 14px;
    }

    .spinner {
      width: 56px;
      height: 56px;
      border: 4px solid var(--teal-lt);
      border-top-color: var(--teal);
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 28px;
    }

    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
    }

    .results-header h2 {
      font-family: 'Instrument Serif', serif;
      font-size: 32px;
      font-weight: 400;
      letter-spacing: -0.8px;
      color: var(--ink);
    }

    .btn-secondary {
      background: transparent;
      color: var(--ink2);
      border: 1.5px solid var(--border);
      padding: 11px 22px;
      border-radius: var(--r-full);
      font-weight: 500;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-secondary:hover {
      border-color: var(--teal);
      color: var(--teal);
      background: var(--teal-lt);
    }

    .result-card {
      background: var(--bg2);
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 28px;
      margin-bottom: 20px;
      transition: all 0.25s;
    }

    .result-card:hover {
      box-shadow: var(--shadow-sm);
    }

    .result-card h3 {
      font-family: 'Instrument Serif', serif;
      font-size: 20px;
      font-weight: 400;
      margin-bottom: 18px;
      color: var(--ink);
    }

    .classification {
      display: flex;
      gap: 16px;
      align-items: center;
      flex-wrap: wrap;
    }

    .category {
      font-size: 18px;
      font-weight: 600;
      color: var(--teal);
      background: var(--teal-lt);
      padding: 8px 16px;
      border-radius: var(--r-sm);
      border: 1px solid var(--teal-mid);
    }

    .confidence {
      color: var(--ink3);
      font-size: 14px;
    }

    .risk-level {
      margin-bottom: 18px;
    }

    .risk-badge {
      display: inline-block;
      padding: 10px 20px;
      border-radius: var(--r-sm);
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 0.5px;
    }

    .risk-critical .risk-badge {
      background: var(--red-lt);
      color: var(--red);
      border: 1px solid #f5b5b0;
    }

    .risk-high .risk-badge {
      background: var(--amber-lt);
      color: var(--amber);
      border: 1px solid #f5c98f;
    }

    .risk-medium .risk-badge {
      background: #edf4ff;
      color: #3b7dd8;
      border: 1px solid #b8d4f7;
    }

    .risk-low .risk-badge {
      background: var(--teal-lt);
      color: var(--teal);
      border: 1px solid var(--teal-mid);
    }

    .issue-counts {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .count {
      padding: 6px 14px;
      border-radius: var(--r-full);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.3px;
    }

    .count.critical {
      background: var(--red-lt);
      color: var(--red);
      border: 1px solid #f5b5b0;
    }

    .count.high {
      background: var(--amber-lt);
      color: var(--amber);
      border: 1px solid #f5c98f;
    }

    .count.medium {
      background: #edf4ff;
      color: #3b7dd8;
      border: 1px solid #b8d4f7;
    }

    .summary {
      line-height: 1.7;
      color: var(--ink2);
      font-size: 15px;
    }

    .issues-list {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .issue {
      border-left: 3px solid;
      padding: 20px;
      background: #fff;
      border-radius: var(--r-sm);
      transition: all 0.2s;
    }

    .issue:hover {
      box-shadow: var(--shadow-sm);
    }

    .issue.severity-critical {
      border-color: var(--red);
      background: linear-gradient(to right, var(--red-lt), #fff);
    }

    .issue.severity-high {
      border-color: var(--amber);
      background: linear-gradient(to right, var(--amber-lt), #fff);
    }

    .issue.severity-medium {
      border-color: #3b7dd8;
      background: linear-gradient(to right, #edf4ff, #fff);
    }

    .issue-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      gap: 12px;
    }

    .issue-title {
      font-weight: 600;
      font-size: 15px;
      color: var(--ink);
    }

    .severity-badge {
      padding: 4px 10px;
      border-radius: var(--r-full);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      flex-shrink: 0;
    }

    .severity-critical .severity-badge {
      background: var(--red-lt);
      color: var(--red);
    }

    .severity-high .severity-badge {
      background: var(--amber-lt);
      color: var(--amber);
    }

    .severity-medium .severity-badge {
      background: #edf4ff;
      color: #3b7dd8;
    }

    .issue-text {
      font-style: italic;
      color: var(--ink3);
      margin: 10px 0;
      font-size: 14px;
      line-height: 1.6;
    }

    .issue-explanation {
      color: var(--ink2);
      margin: 10px 0;
      font-size: 14px;
      line-height: 1.65;
    }

    .issue-recommendations {
      margin-top: 14px;
      padding: 16px;
      background: var(--bg2);
      border-radius: var(--r-sm);
      border: 1px solid var(--border);
    }

    .issue-recommendations strong {
      color: var(--ink);
      font-size: 13px;
    }

    .issue-recommendations ul {
      margin: 10px 0 0 20px;
    }

    .issue-recommendations li {
      margin: 6px 0;
      color: var(--ink2);
      font-size: 14px;
      line-height: 1.6;
    }

    .recommendations ul {
      margin: 0;
      padding-left: 20px;
    }

    .recommendations li {
      margin: 10px 0;
      color: var(--ink2);
      line-height: 1.7;
      font-size: 14px;
    }

    .collapsible h3 {
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: color 0.2s;
    }

    .collapsible h3:hover {
      color: var(--teal);
    }

    .toggle {
      color: var(--ink4);
      font-size: 14px;
    }

    .extracted-text {
      margin-top: 18px;
    }

    .extracted-text pre {
      background: #fff;
      padding: 20px;
      border-radius: var(--r-sm);
      overflow-x: auto;
      white-space: pre-wrap;
      word-wrap: break-word;
      font-size: 13px;
      line-height: 1.7;
      color: var(--ink2);
      border: 1px solid var(--border);
    }

    .error-message {
      text-align: center;
      padding: 60px 40px;
      color: var(--red);
    }

    .error-message span {
      font-size: 56px;
      margin-bottom: 20px;
      display: block;
    }

    .error-message p {
      font-size: 16px;
      margin-bottom: 24px;
      color: var(--ink2);
    }

    .error-message button {
      background: var(--teal);
      color: white;
      border: none;
      padding: 12px 28px;
      border-radius: var(--r-full);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 12px rgba(0, 168, 138, 0.28);
      transition: all 0.2s;
    }

    .error-message button:hover {
      background: #009a7e;
      transform: translateY(-1px);
    }

    @media (max-width: 768px) {
      .upload-container {
        padding: 40px 24px;
      }

      .upload-card {
        padding: 32px 24px;
      }

      h1 {
        font-size: 32px;
      }

      .results-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
      }
    }
  `]
})
export class UploadComponent {
  isDragging = signal(false);
  isAnalyzing = signal(false);
  processingStatus = signal('');
  result = signal<DocumentAnalysis | null>(null);
  error = signal('');
  showText = signal(false);

  constructor(private documentService: DocumentService) {}

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(true);
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(false);
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging.set(false);
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.uploadFile(files[0]);
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.uploadFile(file);
    }
  }

  uploadFile(file: File) {
    // Validate file
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      this.error.set('File too large. Maximum size is 10MB.');
      return;
    }

    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
      this.error.set('Invalid file type. Please upload PDF, JPG, or PNG.');
      return;
    }

    // Upload and analyze
    this.isAnalyzing.set(true);
    this.error.set('');
    this.processingStatus.set('Uploading document...');

    this.documentService.uploadDocument(file).subscribe({
      next: (response) => {
        this.processingStatus.set('Analysis complete!');
        this.result.set(response);
        this.isAnalyzing.set(false);
      },
      error: (err) => {
        this.isAnalyzing.set(false);
        this.error.set(err.error?.error || 'Failed to analyze document. Please try again.');
      }
    });
  }

  reset() {
    this.result.set(null);
    this.error.set('');
    this.showText.set(false);
  }

  toggleText() {
    this.showText.update(v => !v);
  }

  formatCategory(category: string): string {
    return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  formatIssue(issue: string): string {
    return issue.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }
}
