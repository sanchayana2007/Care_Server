import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ServiceProviderService {

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

  getServices(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/service/provider', {
      headers: this.headers
    });
  }
  getService_list(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist', {
      headers: this.headers
    });
  }
  getServiceList(id, verified): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/service/provider?serviceId=' + id , {
      headers: this.headers,
      params: {
      verified : verified
      }
    });
  }
  addServiceList(body): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl +
    '/web/api/service/provider', body,  {
      headers: this.headers
    });
  }


}

