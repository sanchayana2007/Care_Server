import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NotificationsService {

  public static dialogResult = false;
  headers: any;
  id: any;
  constructor(private http: HttpClient) {
  }

  updateToken(xAuth: string, xOrg: string, xApi: string, id: string): void {
    this.id = id;
    this.headers = {
      Authorization: 'Bearer ' + xAuth,
      'x-Origin-Key': xOrg,
      'x-Api-Key': xApi
    };
  }
  getTourTransport(serviceType: number): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl + '/web/api/service/provider', {
      headers: this.headers,
      params: {
        id: this.id
      }
    });
  }
  firstImageSubmit(body, addres): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
      '/web/api/service/provider', body, {
        headers: this.headers,
        params: {
          serviceId: this.id,
          address: addres,
          idType: 'document'
        }
      });
  }
  secondtImageSubmit(body, addres): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
      '/web/api/service/provider', body, {
        headers: this.headers,
        params: {
          serviceId: this.id,
          address: addres,
          idType: 'declaration'
        }
      });
  }
}
