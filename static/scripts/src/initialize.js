/*
    Application bootstrapper and initializer.
 */

define([
    'underscore',
    'jquery',
    'backbone',
    'app/router',
    'app/namespace',
    'nprogress',
    'fastclick',

    'model/card-monster-type',
    'model/card-set',
    'model/card-status',
    'model/card-type',
    'model/card-version',
    'model/card',
    'model/monster-attribute',
    'model/monster-type',
    'model/rarity',
    'model/spell-trap-property',
    'model/user-card-version',
    'model/user-card',
    'model/deck-card',
    'model/deck',

    'bootstrap',
    'jquery.cookie',
    'backbone.chaining'
], function (_, $, Backbone, Router, Namespace, NProgress, FastClick,

        CardMonsterType, CardSet, CardStatus, CardType,
        CardVersion, Card, MonsterAttribute, MonsterType, Rarity,
        SpellTrapProperty, UserCardVersion, UserCard) {

    var bootstrapModels = {
            cardTypes: CardType,
            monsterTypes: MonsterType,
            monsterAttributes: MonsterAttribute,
            rarities: Rarity,
            cardStatuses: CardStatus,
            spellTrapProperties: SpellTrapProperty,
            cardSets: CardSet
        },
        instances = {},
        $document = $(document);

    $document.ready(function () {
        var router;

        // Set up global headers.
        $.ajaxSetup({
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            }
        });

        $(document).ajaxStart(NProgress.start);
        $(document).ajaxStop(NProgress.done);

        FastClick.attach(document.body);

        if (window.bootstrapData) {
            // Instantiate Models.
            _.each(bootstrapModels, function (constructor, key) {
                instances[key] = new Backbone.Collection(
                    window.bootstrapData[key],
                    { model: constructor }
                );
            });
        }

        Namespace.instances = instances;

        // Instantiate Router and make sure links are not reloading the page.
        router = new Router();

        Backbone.history.start({
            pushState: true,
            hashChange: false
        });

        $document.on('click', 'a', function (ev) {
            var $this = $(this),
                href = $this.attr('href');

            if ($this.hasClass('follow')) {
                ev.preventDefault();
                router.navigate(href, { trigger: true });
                return false;
            }
        });
    });

});