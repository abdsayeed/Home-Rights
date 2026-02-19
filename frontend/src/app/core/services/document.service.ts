import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface DocumentAnalysis {
  document_id: string;
  status: string;
  extracted_text: string;
  classification: {
    category: string;
    confidence: number;
  };
  detected_issues: Array<{
    issue: string;
    severity: string;
    matched_text: string;
    explanation: string;
    recommendations: string[];
  }>;
  severity_analysis: {
    overall_risk: string;
    critical_count: number;
    high_count: number;
    medium_count: number;
  };
  summary: string;
  recommendations: string[];
  warning?: string;
  analysis_tier?: string;
}

export interface DocumentListItem {
  document_id: string;
  fileName: string;
  fileType: string;
  status: string;
  createdAt: string;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private apiUrl = `${environment.apiUrl}/documents`;

  constructor(private http: HttpClient) {}

  uploadDocument(file: File): Observable<DocumentAnalysis> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<DocumentAnalysis>(`${this.apiUrl}/upload`, formData);
  }

  analyzeText(text: string, context?: string): Observable<DocumentAnalysis> {
    return this.http.post<DocumentAnalysis>(`${this.apiUrl}/analyze`, { text, context });
  }

  getDocument(documentId: string): Observable<DocumentAnalysis> {
    return this.http.get<DocumentAnalysis>(`${this.apiUrl}/${documentId}`);
  }

  listDocuments(): Observable<{ documents: DocumentListItem[] }> {
    return this.http.get<{ documents: DocumentListItem[] }>(this.apiUrl);
  }
}
