import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ListSpotsComponent } from './list-spots.component';

describe('ListSpotsComponent', () => {
  let component: ListSpotsComponent;
  let fixture: ComponentFixture<ListSpotsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ListSpotsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListSpotsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
