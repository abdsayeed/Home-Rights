import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Topic {
  id: string;
  title: string;
  description: string;
  category: string;
  content: string;
  relatedTopics: string[];
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface TopicCategory {
  category: string;
  count: number;
}

@Injectable({
  providedIn: 'root'
})
export class TopicsService {
  private apiUrl = `${environment.apiUrl}/topics`;

  constructor(private http: HttpClient) {}

  getTopics(category?: string, search?: string): Observable<{ topics: Topic[] }> {
    let url = this.apiUrl;
    const params: string[] = [];
    
    if (category) params.push(`category=${encodeURIComponent(category)}`);
    if (search) params.push(`search=${encodeURIComponent(search)}`);
    
    if (params.length > 0) {
      url += '?' + params.join('&');
    }
    
    return this.http.get<{ topics: Topic[] }>(url);
  }

  getTopic(topicId: string): Observable<Topic> {
    return this.http.get<Topic>(`${this.apiUrl}/${topicId}`);
  }

  getCategories(): Observable<{ categories: TopicCategory[] }> {
    return this.http.get<{ categories: TopicCategory[] }>(`${this.apiUrl}/categories`);
  }

  searchTopics(query: string): Observable<{ topics: Topic[] }> {
    return this.http.get<{ topics: Topic[] }>(`${this.apiUrl}?search=${encodeURIComponent(query)}`);
  }
}
