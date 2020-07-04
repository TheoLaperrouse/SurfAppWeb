import { Component, OnInit } from '@angular/core';
import { ListSpotsComponent } from '../list-spots/list-spots.component';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit {
  res: String;
  constructor() { }

  ngOnInit(): void {
  }

}
