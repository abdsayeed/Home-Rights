import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface SupportOrganization {
  id: string;
  name: string;
  type: string;
  description: string;
  services: string[];
  contact: {
    phone?: string;
    email?: string;
    website?: string;
    address?: string;
  };
  location: {
    city?: string;
    region?: string;
    postcode?: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
  };
  availability: {
    hours?: string;
    languages?: string[];
  };
  rating?: number;
  distance?: number;
}

@Injectable({
  providedIn: 'root'
})
export class SupportService {
  private apiUrl = `${environment.apiUrl}/support`;

  constructor(private http: HttpClient) {}

  findSupport(params: {
    location?: string;
    issue_type?: string;
    service_type?: string;
    max_distance?: number;
  }): Observable<{ organizations: SupportOrganization[] }> {
    const queryParams: string[] = [];
    
    if (params.location) queryParams.push(`location=${encodeURIComponent(params.location)}`);
    if (params.issue_type) queryParams.push(`issue_type=${encodeURIComponent(params.issue_type)}`);
    if (params.service_type) queryParams.push(`service_type=${encodeURIComponent(params.service_type)}`);
    if (params.max_distance) queryParams.push(`max_distance=${params.max_distance}`);
    
    const url = queryParams.length > 0 ? `${this.apiUrl}?${queryParams.join('&')}` : this.apiUrl;
    
    return this.http.get<{ organizations: SupportOrganization[] }>(url);
  }

  getOrganization(orgId: string): Observable<SupportOrganization> {
    return this.http.get<SupportOrganization>(`${this.apiUrl}/${orgId}`);
  }
}
