import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AUTHGWCONSTANTS } from '../../../authorization/authconstants';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ProdectsService {

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
  getProdectList(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/service/product', {
      headers: this.headers
    });
  }
  getServiceList(): Observable<any> {
    return this.http.get<any>(environment.proxyApiUrl +
    '/web/api/med/servicelist', {
      headers: this.headers,
    });
  }
  addProduct(body): Observable<any> {
    return this.http.post<any>(environment.proxyApiUrl +
    '/web/api/service/product', body,  {
      headers: this.headers
    });
  }
  editProduct(body): Observable<any> {
    return this.http.put<any>(environment.proxyApiUrl +
    '/web/api/service/product', body,  {
      headers: this.headers
    });
  }

  deleteProduct(id): Observable<any> {
    return this.http.delete<any>(environment.proxyApiUrl +
    '/web/api/service/product', {
      headers: this.headers,
      params: { id: id }
    });
  }
}
