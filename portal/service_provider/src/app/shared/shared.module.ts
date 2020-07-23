import { Subject } from 'rxjs';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@NgModule({
  imports: [CommonModule],
  declarations: []
})
export class SharedModule {

  public static GWwebSocket = null;

  involeselectedEvent: Subject<any> = new Subject();
  invokeWebsocket: Subject<any> = new Subject();
  invokeWebsocketInstant: Subject<any> = new Subject();
  invokeWebsocketclose: Subject<any> = new Subject();
  invokeWsInstant: Subject<any> = new Subject();
  invokeCreatews: Subject<any> = new Subject();
  involeselect_unselectEvent: Subject<any> = new Subject();
  private globalmessage = new Subject<any>();

  selected_vehicle(selectedVehicle) {
    return this.involeselectedEvent.next(selectedVehicle);
  }
  sendwsmessage(message) {
    return this.invokeWebsocket.next(message);
  }
  wsInstant(ws) {
    return this.invokeWebsocketInstant.next(ws);
  }
  socketClose(data) {
    return this.invokeWebsocketclose.next(data);
  }
  callWebsocket(data) {
    return this.invokeCreatews.next(data);
  }
  sendwsInstant(data) {
    return this.invokeWsInstant.next(data);
  }
}
