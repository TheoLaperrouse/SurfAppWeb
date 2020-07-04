import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
@Component({
  selector: 'app-add-spot',
  templateUrl: './add-spot.component.html',
  styleUrls: ['./add-spot.component.scss']
})
export class AddSpotComponent implements OnInit {

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit(): void {
  }
  addSpot(): void {
    var nomSpot = (<HTMLInputElement>document.getElementById('nomSpot')).value
    var pointsGeo = (<HTMLInputElement>document.getElementById('pointsGeo')).value
    var orientationPlage = (<HTMLInputElement>document.getElementById('orientationPlage')).value
    var spotToSend = {}
    spotToSend['nomSpot'] = nomSpot
    spotToSend['pointsGeo'] = pointsGeo
    spotToSend['orientationPlage'] = orientationPlage
    this.httpClient.post('http://127.0.0.1:5002/addSpot', spotToSend).subscribe(data => {
      console.log(spotToSend)
    })
  }

}
