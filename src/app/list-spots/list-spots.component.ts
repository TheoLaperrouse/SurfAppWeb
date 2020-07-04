import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Component({
  selector: 'app-list-spots',
  templateUrl: './list-spots.component.html',
  styleUrls: ['./list-spots.component.scss']
})
export class ListSpotsComponent implements OnInit {
  spots: JSON;
  bestSpots: JSON;
  res: String;
  arrayRes: Array<String>;
  constructor(private httpClient: HttpClient) {
  }


  ngOnInit(): void {
    this.httpClient.get('http://127.0.0.1:5002/').subscribe(data => {
      this.spots = data['spots'] as JSON;
      console.log(this.spots);
    })
  }
  goTo(pointsGeo, spotName, orientationPlage): void {
    var URL = 'http://127.0.0.1:5002/bestsRide'
    let parametres = new HttpParams();
    parametres = parametres.append('pointGeo', pointsGeo);
    parametres = parametres.append('nomSpot', spotName);
    parametres = parametres.append('orientationPlage', orientationPlage)
    console.log(parametres)
    this.httpClient.get(URL, { params: parametres }).subscribe(data => {
      this.bestSpots = data as JSON;
      console.log(data['spots'])
      this.arrayRes = []
      for (let spot of data['spots']) {
        console.log(spot)
        var toAdd = spot.location + ': Score ' + spot.score + '\n' + spot.date + ' à ' + spot.hours + '\nLe vent soufflera vers ' + spot.directionVent + ' à ' + spot.vitesseVent + ' km / s\n'
        console.log(toAdd)
        this.arrayRes.push(toAdd)
      }
      this.res = ''
      this.res = this.arrayRes.join('\n')
    })
  }
}