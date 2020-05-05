import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ServiceListService {

  public static dialogResult = false;
  xOriginKey = environment.xOrigin.key;
  xApiKey = environment.xApi.key;
  headers: any;
  httpClient: any;

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

  getServiceList(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist', {
      headers: this.headers
    });
  }

  addServiceList(body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist', body, {
      headers: this.headers
    });
  }

  editServiceList(body): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist', body, {
      headers: this.headers
    });
  }

  uploadServiceImage(id, body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
      '/web/api/med/servicemedia?id=' + id, body, {
      headers: this.headers
    });
  }

  deleteServiceList(id): Observable<any> {
    return this.http.delete<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist?id=' + id, {
      headers: this.headers,
    });
  }
}
