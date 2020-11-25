import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SmsService {

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
  addSms(body: any): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/component/send/sms', body, {
      headers: this.headers
    });
  }
  getSmsCreadits(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/component/send/sms', {
      headers: this.headers
    });
  }
}

