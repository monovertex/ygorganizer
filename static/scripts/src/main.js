
require.config({
    baseUrl: '/static/scripts/lib',

    paths: {
        app: '../src',
        view: '../src/view',
        model: '../src/model',
        collection: '../src/collection',
        templates: '../../templates/build'
    },

    shim: {
        'bootstrap': ['jquery']
    },

});

require(['app/initialize']);