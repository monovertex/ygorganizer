

define([
    'underscore',
    'backbone',
    'model/card',
    'backbone.relational'
], function (_, Backbone, Card) {

    return Backbone.RelationalModel.extend({

        url: '/api/deck/',

        relations: [
            {
                key: 'card',
                relatedModel: Card,
                type: 'HasOne',
                reverseRelation: {
                    key: 'deck_cards',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            }
        ]

    });

});