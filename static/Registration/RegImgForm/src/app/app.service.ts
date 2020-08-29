import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  public static dialogResult = false;
  headers: any;
  id: any;
  constructor(private http: HttpClient) {
    // this.headers = {
    //   Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MjQ3ODcwNzAsImtleSI6ImdBQUFBQUJlOXhULVdUYkRWNmx2VHF4blJ1aVBuLVRuVzFtRUFZWl9uUW1TeEpfeEY5VG1nMVR4aVpWWXhMNUNlUUFzTFU2VmhFTHI0RzhyUzF2X1JxT3lTSTNrWkJTN3lRZkZNMHBUcUppMXEwRzBwT3ZmeE93PSJ9.a3t-eJMo7inzC5xA-DlDke1MDG6MEk3KCPD8HWnnGng',
    //   'x-Origin-Key': 'gAAAAABeka_J124HZJ0ERgFU_K7L3HeMFCUMaqRXuPd0SaaBzO09BdndXhZPROmE2DKwMqvWbGEiAtbIe1BVRAC_olGghhy9rM8j6ztXt5xOpwuI_SjMywQ=',
    //   'x-Api-Key': 'gAAAAABe9xT-6hLHgcpItRGh3NtJJcRNX3geuQsaSwuHdKWM2r4oU6Oegq4PC2zFNnQOU0_DSB8AtLWun6GKu5Jae71XeRBhi4JlAtFvs7o57u3QGFVQOi0='
    // };
  }

  updateToken(xAuth: string, xOrg: string, xApi: string, id: string): void{
    this.id = id;
    this.headers = {
      Authorization: 'Bearer ' + xAuth,
      'x-Origin-Key': xOrg,
      'x-Api-Key': xApi
    };
  }
  getService_list(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist', {
      headers: this.headers
    });
  }
  getState(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/state/info', {
      headers: this.headers
    });
  }
  getDistricts(district): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/district/info?state=' + district, {
      headers: this.headers
    });
  }
  getAreas(place): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/place/info?district=' + place , {
      headers: this.headers
    });
  }
  getServices(serviceType: number): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
       '/web/api/service/provider/v2', {
      headers: this.headers,
      params: {
        id: this.id
      }
    });
  }
  postData(queryParam, body): Observable<any> {
    return this.http.post<any>(
       environment.proxyApiUrl +
      '/web/api/service/provider/v2?', body, {
        headers: this.headers,
        params: queryParam
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
