import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProdectsAddDialogComponent } from './prodects-add-dialog.component';

describe('ProdectsAddDialogComponent', () => {
  let component: ProdectsAddDialogComponent;
  let fixture: ComponentFixture<ProdectsAddDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProdectsAddDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProdectsAddDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
