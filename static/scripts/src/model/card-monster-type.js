

define([
    'backbone',
    'model/monster-type',

    'backbone.relational'
], function (Backbone, MonsterType) {

    return Backbone.RelationalModel.extend({

        relations: [
            {
                key: 'monster_type',
                relatedModel: MonsterType,
                type: 'HasOne',
                reverseRelation: {
                    key: 'card_monster_types',
                    includeInJSON: 'id'
                },
                includeInJSON: 'id'
            }
        ]

    });

});