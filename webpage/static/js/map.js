const loadingIcon = document.querySelector('.loading-icon');

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        })
    ],
    view: new ol.View({
        center: [-81, 27],
        zoom: 6,
        projection: 'EPSG:4326'
    })
});

const vectorSource = new ol.source.Vector({
});
const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'gba(46, 204, 113, 1)',
            width: 2
        }),
        image: new ol.style.Circle({
            radius: 4,
            fill: new ol.style.Fill({
                color: 'rgba(46, 204, 113, 0.9)'
            })
        })
    })
});
map.addLayer(vectorLayer);

const vectorSource2 = new ol.source.Vector({
});
const vectorLayer2 = new ol.layer.Vector({
    source: vectorSource2,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'red',
            width: 2
        }),
        image: new ol.style.Circle({
            radius: 4,
            fill: new ol.style.Fill({
                color: 'rgba(255, 0, 0, 0.9)'
            })
        })
    })
});
map.addLayer(vectorLayer2);


const vectorSource3 = new ol.source.Vector({
});
const vectorLayer3 = new ol.layer.Vector({
    source: vectorSource3,
    style: new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(252, 214, 112, 0.4)'
        }),
        stroke: new ol.style.Stroke({
            color: 'rgba(252, 214, 112, 1)',
            width: 2
        }),

    })
});
map.addLayer(vectorLayer3);


function queryHandler(data0) {
    loadingIcon.style.display = 'none';
    data = $.parseJSON(data0['greenhouse'])
    data2 = $.parseJSON(data0['redhouse'])
    data3 = $.parseJSON(data0['yellowhurricane'])
    vectorSource.clear(true);
    vectorSource.addFeatures(new ol.format.GeoJSON().readFeatures(data));

    vectorSource2.clear(true);
    vectorSource2.addFeatures(new ol.format.GeoJSON().readFeatures(data2));

    vectorSource3.clear(true);
    vectorSource3.addFeatures(new ol.format.GeoJSON().readFeatures(data3));
}

function doQuery(year, quarter) {
    loadingIcon.style.display = 'block';
    $.ajax({
        url: '/filter?year='
            + year
            + '&quarter='
            + quarter,
        dataType: 'json',
        success: queryHandler
    });

}

function doClearall() {
    vectorSource.clear();
    vectorSource.refresh();

    vectorSource2.clear();
    vectorSource2.refresh();

    vectorSource3.clear();
    vectorSource3.refresh();
}

const selectStyle = new ol.style.Style({
    text: new ol.style.Text(),
    image: new ol.style.Circle({
        radius: 4,
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.9)'
        })
    })
});

let selected = null;
map.on('pointermove', function (e) {
    if (selected !== null) {
        selected.setStyle(undefined);
        selected = null;
    }

    var hit = map.forEachFeatureAtPixel(e.pixel, function (f) {
        if (f.get('Address') == undefined) return false;
        selected = f;
        selectStyle.getText().setText(f.get('Address'));
        f.setStyle(selectStyle);
        return true;
    });

    if (hit) {
        this.getTargetElement().style.cursor = 'pointer';
    } else {
        this.getTargetElement().style.cursor = '';
    }

});
