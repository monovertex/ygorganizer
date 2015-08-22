

define([
    'backbone',
    'model/card-set',
    'model/rarity',
    'model/user-card-version',
    'model/card',

    'backbone.relational'
], function (Backbone, CardSet, Rarity, UserCardVersion, Card) {

    return Backbone.RelationalModel.extend({

        relations: [
            {
                key: 'card_set',
                relatedModel: CardSet,
                type: 'HasOne',
                reverseRelation: {
                    key: 'card_versions',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'rarity',
                relatedModel: Rarity,
                type: 'HasOne',
                reverseRelation: {
                    key: 'card_versions',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'user_card_version',
                relatedModel: UserCardVersion,
                type: 'HasOne',
                reverseRelation: {
                    key: 'card_version',
                    type: 'HasOne',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'card',
                relatedModel: Card,
                type: 'HasOne',
                reverseRelation: {
                    key: 'card_versions'
                }
            }
        ]

    });

});