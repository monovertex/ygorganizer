

define([
    'underscore',
    'backbone',
    'model/card-type',
    'model/card-status',
    'model/spell-trap-property',
    'model/monster-attribute',
    'model/card-monster-type',
    'model/user-card',

    'backbone.relational'
], function (_, Backbone, CardType, CardStatus, SpellTrapProperty,
        MonsterAttribute, CardMonsterType, UserCard) {

    var Card = Backbone.RelationalModel.extend({

        urlRoot: '/api/cards/',

        url: function () {
            return this.urlRoot + this.get('identifier') + '/';
        },

        relations: [
            {
                key: 'card_type',
                relatedModel: CardType,
                type: 'HasOne',
                reverseRelation: {
                    key: 'cards',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'status_traditional',
                relatedModel: CardStatus,
                type: 'HasOne',
                reverseRelation: {
                    key: 'traditional_cards',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'status_advanced',
                relatedModel: CardStatus,
                type: 'HasOne',
                reverseRelation: {
                    key: 'advanced_cards',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'spell_trap_property',
                relatedModel: SpellTrapProperty,
                type: 'HasOne',
                reverseRelation: {
                    key: 'cards',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'monster_attribute',
                relatedModel: MonsterAttribute,
                type: 'HasOne',
                reverseRelation: {
                    key: 'cards',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'card_monster_types',
                relatedModel: CardMonsterType,
                type: 'HasMany',
                reverseRelation: {
                    key: 'card',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            },
            {
                key: 'user_card',
                relatedModel: UserCard,
                type: 'HasOne',
                reverseRelation: {
                    key: 'card',
                    includeInJSON: 'id',
                    type: 'HasOne',
                },
                includeInJSON: 'id'
            }
        ]

    }, {
        findModel: function (attributes) {
            var model = Backbone.Relational.store.find(Card, attributes);

            if (!model && _.isObject(attributes)) {
                var collection = Backbone.Relational.store.getCollection(Card);

                model = collection.find(function (m) {
                    return m.get('identifier') === attributes.identifier;
                });
            }

            return model;
        }
    });

    return Card;

});