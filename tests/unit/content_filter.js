define('tests/unit/content_filter',
    ['tests/unit/helpers'],
    function(helpers) {

    function meowEnabled(injector) {
        return injector.mock('core/settings', {
            meowEnabled: true
        });
    }

    function noStorage(injector) {
        return injector.mock('core/storage', {
            getItem: function() { return null; },
            setItem: function() { return null; },
        });
    }

    function desktopCapabilities(injector) {
        return injector.mock('core/capabilities', {
            device_platform: function() { return 'desktop'; },
            device_formfactor: function() { return ''; },
            device_type: function() { return 'desktop'; },
            os: {type: 'desktop'},
        });
    }

    function firefoxOSCapabilities(injector) {
        return injector.mock('core/capabilities', {
            device_platform: function() { return 'firefoxos'; },
            device_formfactor: function() { return ''; },
            device_type: function() { return 'firefoxos'; },
            firefoxOS: true,
            os: {},
        });
    }

    describe.only('content_filter', function() {
        it('is webapp on desktop',
            helpers
            .injector(desktopCapabilities, noStorage, meowEnabled)
            .run(['content_filter'], function(contentFilter) {
                var args = contentFilter.apiArgs('search');
                assert.equal(args.doc_type, 'webapp');
            }));

        it('is all by default on firefoxos',
            helpers
            .injector(firefoxOSCapabilities, noStorage, meowEnabled)
            .run(['content_filter'], function(contentFilter) {
                var args = contentFilter.apiArgs('search');
                assert.equal(args.doc_type, 'all');
            }));

        it('is webapp not meowEnabled',
            helpers
            .injector(firefoxOSCapabilities, noStorage)
            .run(['content_filter'], function(contentFilter) {
                var args = contentFilter.apiArgs('search');
                assert.equal(args.doc_type, 'webapp');
            }));
    });
});
