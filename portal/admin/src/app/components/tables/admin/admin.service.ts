import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  public static dialogResult = false;
  xOriginKey = environment.xOrigin.key;
  xApiKey = environment.xApi.key;
  headers: any;
  constructor(private http: HttpClient) {
    const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
    // const xOriginKey = localStorage.getItem(AUTHGWCONSTANTS.xOriginKey);
    // const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
    this.headers = {
      Authorization: 'Bearer ' + token,
      'x-Origin-Key': this.xOriginKey,
      'x-Api-Key': this.xApiKey
    };
  }

  getAdmins(closed: number): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/resource/admin?closed=' + closed, {
      headers: this.headers
    });
  }

  addAdmins(body: any): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/resource/admin', body, {
      headers: this.headers
    });
  }

  editAdmins(body): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl +
    '/web/api/resource/admin?closed=0', body, {
      headers: this.headers
    });
  }

  // deleteAdmins(id): Observable<any> {
  //   return this.http.delete<any>(environment.proxyApiUrl +
  //   '/web/api/resource/admin', {
  //     headers: this.headers,
  //     params: { id: id }
  //   });
  // }
}

