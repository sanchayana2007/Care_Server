import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DashCardVerticalComponent } from './dash-card-vertical.component';

describe('DashCardVerticalComponent', () => {
  let component: DashCardVerticalComponent;
  let fixture: ComponentFixture<DashCardVerticalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DashCardVerticalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashCardVerticalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
