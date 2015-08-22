

define([
    'underscore',
    'backbone',
    'model/deck-card',
    'backbone.relational'
], function (_, Backbone, DeckCard) {

    return Backbone.RelationalModel.extend({

        relations: [
            {
                key: 'deck_cards',
                relatedModel: DeckCard,
                type: 'HasMany',
                reverseRelation: {
                    key: 'deck',
                    includeInJSON: false
                },
                includeInJSON: true
            },
            {
                key: 'deck_cards_main',
                relatedModel: DeckCard,
                type: 'HasMany',
                includeInJSON: false
            },
            {
                key: 'deck_cards_extra',
                relatedModel: DeckCard,
                type: 'HasMany',
                includeInJSON: false
            },
            {
                key: 'deck_cards_side',
                relatedModel: DeckCard,
                type: 'HasMany',
                includeInJSON: false
            }
        ]

    });

});