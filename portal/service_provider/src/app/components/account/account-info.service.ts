import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../authorization/authconstants';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AccountInfoService {

  public static dialogResult = true;
  xOriginKey = environment.xOrigin.key;
  xApiKey = environment.xApi.key;
  headers: any;
  constructor(private http: HttpClient) {
    const token = localStorage.getItem(AUTHGWCONSTANTS.bearerToken);
    // const xOriginKey = localStorage.getItem(AUTHGWCONSTANTS.xOriginKey);
    const xApiKey = localStorage.getItem(AUTHGWCONSTANTS.xApiKey);
    this.headers = {
      Authorization: 'Bearer ' + token,
      'x-Origin-Key': this.xOriginKey,
      'x-Api-Key': xApiKey
    };
  }

  getHomePage(id): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/account/overview?id=' + id, {
      headers: this.headers
    });
  }

  postAccountValue(body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/service/hotel', body, {
      headers: this.headers
    });
  }

  getServiceFrom(method: Number): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/service/hotel', {
      headers: this.headers,
      params: {
        method: method.toString(),
      }
    });
  }

  getDocumentDetails(method: Number): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/service/hotel', {
      headers: this.headers,
      params: {
        method: method.toString(),
      }
    });
  }

  documentSubmit(method: Number, idNumber, body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/service/account/document/upload', body, {
      headers: this.headers,
      params: {
        method: method.toString(),
        idNumber: idNumber,
      }
    });
  }

  goodImageSubmit(method: Number, body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/service/account/image/upload', body, {
      headers: this.headers,
      params: {
        method: method.toString(),
      }
    });
  }

  getPreviewDataInfo(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/service/hotel', {
      headers: this.headers,
    });
  }

  // extra API
  getAdminProfileInfo(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/resource/profile?closed=0', {
      headers: this.headers
    });
  }

  getAccommoCovid19Form(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/covid?serviceType=1', {
      headers: this.headers
    });
  }

  accommoCovid19Form(body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/covid', body, {
      headers: this.headers
    });
  }
}


