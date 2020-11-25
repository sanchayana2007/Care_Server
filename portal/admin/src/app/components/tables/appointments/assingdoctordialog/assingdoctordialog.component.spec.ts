import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AssingdoctordialogComponent } from './assingdoctordialog.component';

describe('AssingdoctordialogComponent', () => {
  let component: AssingdoctordialogComponent;
  let fixture: ComponentFixture<AssingdoctordialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AssingdoctordialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AssingdoctordialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
