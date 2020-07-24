import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { AUTHGWCONSTANTS } from './authconstants';
import { environment } from 'src/environments/environment';

@Injectable()
export class AuthorizationService {

  xOriginKey = environment.xOrigin.key;
  xApiKey = environment.xApi.key;

  headers: any;
  authHeaders: any;
  constructor(private http: HttpClient) {
    this.headers = new Headers();
    // const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
    // const xOriginKey = localStorage.getItem(AUTHGWCONSTANTS.xOriginKey);
    // const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
    this.headers = {
      // Authorization: 'Bearer ' + token,
      'x-Origin-Key': this.xOriginKey,
      // 'x-Api-Key': xApiKey
    };
    // otp header
    this.authHeaders = {
      'x-Origin-Key': this.xOriginKey,
    };
  }

  updateHeaders(): boolean {
    try {
      const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
      // const xOriginKey = localStorage.getItem(AUTHGWCONSTANTS.xOriginKey);
      const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
      this.headers = {
        Authorization: 'Bearer ' + token,
        'x-Origin-Key': this.xOriginKey,
        'x-Api-Key': xApiKey
      };
      return true;
    } catch {
      return false;
    }
  }

  postSignIn(body: any): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
      '/web/api/sign/in', body, {
        headers: this.headers
      });
  }

  postSignUp(body: any): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
      '/web/api/sign/up', body, {
        headers: this.headers
      });
  }

  putOtp(body: any): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl +
      '/web/api/sign/in', body, {
        headers: this.authHeaders
      });
  }

  getAdminProfileInfo(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
      '/web/api/resource/profile?closed=0', {
        headers: this.headers
      });
  }

  getEntityInfo(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl + '/web/entity', {
      headers: this.headers
    });
  }

  getEntityServices(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl + '/web/entity_service', {
      headers: this.headers
    });
  }
}
