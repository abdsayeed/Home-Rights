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
  };
  address?: string;
  location?: {
    city?: string;
    region?: string;
    postcode?: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
  };
  availability?: {
    hours?: string;
    languages?: string[];
  };
  openingHours?: {
    [key: string]: {
      open: string;
      close: string;
    };
  };
  verificationStatus?: string;
  rating?: number;
  distance?: number;
  distanceKm?: number;
}

@Injectable({
  providedIn: 'root'
})
export class SupportService {
  private apiUrl = `${environment.apiUrl}/support`;

  constructor(private http: HttpClient) {}

  findSupport(params: any): Observable<{ organizations: SupportOrganization[], pagination?: any }> {
    const queryParams: string[] = [];
    
    // Map frontend params to backend API params
    if (params.postcode) queryParams.push(`postcode=${encodeURIComponent(params.postcode)}`);
    if (params.lat) queryParams.push(`lat=${params.lat}`);
    if (params.lng) queryParams.push(`lng=${params.lng}`);
    if (params.radius) queryParams.push(`radius=${params.radius}`);
    if (params.service_type) queryParams.push(`type=${encodeURIComponent(params.service_type)}`);
    if (params.page) queryParams.push(`page=${params.page}`);
    if (params.limit) queryParams.push(`limit=${params.limit}`);
    
    const url = `${this.apiUrl}/find${queryParams.length > 0 ? '?' + queryParams.join('&') : ''}`;
    
    return this.http.get<{ organizations: SupportOrganization[], pagination?: any }>(url);
  }

  getOrganization(orgId: string): Observable<SupportOrganization> {
    return this.http.get<SupportOrganization>(`${this.apiUrl}/${orgId}`);
  }

  trackReferral(orgId: string, type: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${orgId}/referral`, { type });
  }
}
