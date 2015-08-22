


define([
    'backbone',

    'view/page/error',
    'view/page/browse',
    'view/page/collection',
    'view/page/deck-list',
    'view/page/deck',
    'view/page/import-rarities'
], function (Backbone, ErrorView, BrowseView, CollectionView,
        DeckListView, DeckView, ImportRaritiesView) {

    return Backbone.Router.extend({

        routes: {
            'collection/(:identifier/)': 'collection',
            'browse/(:identifier/)': 'browse',
            'deck-list/': 'deckList',
            'deck/:id/': 'deck',
            'import/rarities/': 'importRarities',
            '(*default)': 'error',
        },

        collection: function (identifier) {
            this.collectionView = this.collectionView || new CollectionView();
            this.collectionView.render(identifier);
        },

        browse: function (identifier) {
            this.browseView = this.browseView || new BrowseView();

            this.browseView.render(identifier);
        },

        deckList: function () {
            this.deckListView = this.deckListView || new DeckListView();

            this.deckListView.render();
        },

        deck: function (id) {
            this.deckView = this.deckView || new DeckView();

            this.deckView.render(id);
        },

        importRarities: function () {
            this.importRaritiesView = this.importRaritiesView ||
                new ImportRaritiesView();

            this.importRaritiesView.render();
        },

        error: function () {
            this.errorView = this.errorView || new ErrorView();

            this.errorView.render();
        }

    });

});