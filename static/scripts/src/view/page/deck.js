

define([
    'backbone',
    'underscore',
    'jquery',
    'templates',
    'view/component/card',
    'model/deck',
    'view/component/deck',
    'model/card',
    'view/component/card-browser',
], function (Backbone, _, $, Templates, CardView, Deck, DeckView, Card,
        BrowserView) {

    return Backbone.View.extend({

        template: Templates.deck,

        events: {
            'mouseenter .deck-wrapper .card': 'mouseenter',
            'mouseenter .browser-wrapper .card': 'mouseenter'
        },

        initialize: function () {
            this.setElement(this.template());

            this.cardView = new CardView({
                el: this.$('.card-wrapper'),
                rootUrl: this.rootUrl
            });

            this.deckView = new DeckView({
                el: this.$('.deck-wrapper')
            });

            this.browserView = new BrowserView();
        },

        render: function (id) {
            var deck = Deck.findOrCreate({ id: id });

            deck.fetch().done(_.bind(function () {
                this.deckView.model = deck;
                this.deckView.render();

                this.cardView.render(
                    deck.get('deck_cards_main').first().get('card')
                );
            }, this));

            this.browserView.setElement(this.$('.browser-wrapper'));
            this.browserView.render();

            return this;
        },

        mouseenter: function (ev) {
            var card = Card.findOrCreate({
                id: $(ev.currentTarget).data('id')
            });

            this.cardView.render(card);
        }

    });

});