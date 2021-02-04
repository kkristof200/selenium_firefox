# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Prefs ------------------------------------------------------------- #

class Prefs:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: Dict[str, any]
    ):
        self.app_normandy_api_url                                                = d.get('app.normandy.api_url')
        self.app_normandy_first_run                                              = d.get('app.normandy.first_run')
        self.app_normandy_migrations_applied                                     = d.get('app.normandy.migrationsApplied')
        self.app_shield_optoutstudies_enabled                                    = d.get('app.shield.optoutstudies.enabled')
        self.app_update_auto                                                     = d.get('app.update.auto')
        self.app_update_check_install_time                                       = d.get('app.update.checkInstallTime')
        self.app_update_disabled_for_testing                                     = d.get('app.update.disabledForTesting')
        self.app_update_enabled                                                  = d.get('app.update.enabled')
        self.app_update_last_update_time_addon_background_update_timer           = d.get('app.update.lastUpdateTime.addon-background-update-timer')
        self.app_update_last_update_time_background_update_timer                 = d.get('app.update.lastUpdateTime.background-update-timer')
        self.app_update_last_update_time_browser_cleanup_thumbnails              = d.get('app.update.lastUpdateTime.browser-cleanup-thumbnails')
        self.app_update_last_update_time_region_update_timer                     = d.get('app.update.lastUpdateTime.region-update-timer')
        self.app_update_last_update_time_search_engine_update_timer              = d.get('app.update.lastUpdateTime.search-engine-update-timer')
        self.app_update_last_update_time_services_settings_poll_changes          = d.get('app.update.lastUpdateTime.services-settings-poll-changes')
        self.app_update_last_update_time_telemetry_modules_ping                  = d.get('app.update.lastUpdateTime.telemetry_modules_ping')
        self.app_update_last_update_time_xpi_signature_verification              = d.get('app.update.lastUpdateTime.xpi-signature-verification')
        self.apz_content_response_timeout                                        = d.get('apz.content_response_timeout')
        self.browser_eula_3_accepted                                             = d.get('browser.EULA.3.accepted')
        self.browser_eula_override                                               = d.get('browser.EULA.override')
        self.browser_bookmarks_added_import_button                               = d.get('browser.bookmarks.addedImportButton')
        self.browser_bookmarks_restore_default_bookmarks                         = d.get('browser.bookmarks.restore_default_bookmarks')
        self.browser_contentblocking_category                                    = d.get('browser.contentblocking.category')
        self.browser_contentblocking_intro_count                                 = d.get('browser.contentblocking.introCount')
        self.browser_displayed_e10_snotice                                       = d.get('browser.displayedE10SNotice')
        self.browser_dom_window_dump_enabled                                     = d.get('browser.dom.window.dump.enabled')
        self.browser_download_manager_show_when_starting                         = d.get('browser.download.manager.showWhenStarting')
        self.browser_download_panel_shown                                        = d.get('browser.download.panel.shown')
        self.browser_download_viewable_internally_type_was_registered_svg        = d.get('browser.download.viewableInternally.typeWasRegistered.svg')
        self.browser_download_viewable_internally_type_was_registered_webp       = d.get('browser.download.viewableInternally.typeWasRegistered.webp')
        self.browser_download_viewable_internally_type_was_registered_xml        = d.get('browser.download.viewableInternally.typeWasRegistered.xml')
        self.browser_link_open_external                                          = d.get('browser.link.open_external')
        self.browser_link_open_newwindow                                         = d.get('browser.link.open_newwindow')
        self.browser_migration_version                                           = d.get('browser.migration.version')
        self.browser_newtab_url                                                  = d.get('browser.newtab.url')
        self.browser_newtabpage_activity_stream_impression_id                    = d.get('browser.newtabpage.activity-stream.impressionId')
        self.browser_newtabpage_enabled                                          = d.get('browser.newtabpage.enabled')
        self.browser_newtabpage_storage_version                                  = d.get('browser.newtabpage.storageVersion')
        self.browser_offline                                                     = d.get('browser.offline')
        self.browser_page_actions_persisted_actions                              = d.get('browser.pageActions.persistedActions')
        self.browser_pagethumbnails_capturing_disabled                           = d.get('browser.pagethumbnails.capturing_disabled')
        self.browser_pagethumbnails_storage_version                              = d.get('browser.pagethumbnails.storage_version')
        self.browser_reader_detected_first_article                               = d.get('browser.reader.detectedFirstArticle')
        self.browser_region_update_updated                                       = d.get('browser.region.update.updated')
        self.browser_safebrowsing_blocked_ur_is_enabled                          = d.get('browser.safebrowsing.blockedURIs.enabled')
        self.browser_safebrowsing_downloads_enabled                              = d.get('browser.safebrowsing.downloads.enabled')
        self.browser_safebrowsing_enabled                                        = d.get('browser.safebrowsing.enabled')
        self.browser_safebrowsing_malware_enabled                                = d.get('browser.safebrowsing.malware.enabled')
        self.browser_safebrowsing_phishing_enabled                               = d.get('browser.safebrowsing.phishing.enabled')
        self.browser_safebrowsing_provider_mozilla_lastupdatetime                = d.get('browser.safebrowsing.provider.mozilla.lastupdatetime')
        self.browser_safebrowsing_provider_mozilla_nextupdatetime                = d.get('browser.safebrowsing.provider.mozilla.nextupdatetime')
        self.browser_search_region                                               = d.get('browser.search.region')
        self.browser_search_update                                               = d.get('browser.search.update')
        self.browser_selfsupport_url                                             = d.get('browser.selfsupport.url')
        self.browser_sessionstore_resume_from_crash                              = d.get('browser.sessionstore.resume_from_crash')
        self.browser_shell_check_default_browser                                 = d.get('browser.shell.checkDefaultBrowser')
        self.browser_slow_startup_average_time                                   = d.get('browser.slowStartup.averageTime')
        self.browser_slow_startup_samples                                        = d.get('browser.slowStartup.samples')
        self.browser_startup_homepage                                            = d.get('browser.startup.homepage')
        self.browser_startup_homepage_override_mstone                            = d.get('browser.startup.homepage_override.mstone')
        self.browser_startup_last_cold_startup_check                             = d.get('browser.startup.lastColdStartupCheck')
        self.browser_startup_page                                                = d.get('browser.startup.page')
        self.browser_tabs_close_window_with_last_tab                             = d.get('browser.tabs.closeWindowWithLastTab')
        self.browser_tabs_disable_background_zombification                       = d.get('browser.tabs.disableBackgroundZombification')
        self.browser_tabs_remote_separate_privileged_content_process             = d.get('browser.tabs.remote.separatePrivilegedContentProcess')
        self.browser_tabs_warn_on_close                                          = d.get('browser.tabs.warnOnClose')
        self.browser_tabs_warn_on_close_other_tabs                               = d.get('browser.tabs.warnOnCloseOtherTabs')
        self.browser_tabs_warn_on_open                                           = d.get('browser.tabs.warnOnOpen')
        self.browser_toolbars_bookmarks_visibility                               = d.get('browser.toolbars.bookmarks.visibility')
        self.browser_ui_customization_state                                      = d.get('browser.uiCustomization.state')
        self.browser_uitour_enabled                                              = d.get('browser.uitour.enabled')
        self.browser_urlbar_placeholder_name                                     = d.get('browser.urlbar.placeholderName')
        self.browser_urlbar_suggest_searches                                     = d.get('browser.urlbar.suggest.searches')
        self.browser_used_on_windows10_intro_ur_l                                = d.get('browser.usedOnWindows10.introURL')
        self.browser_warn_on_quit                                                = d.get('browser.warnOnQuit')
        self.datareporting_healthreport_about_report_url                         = d.get('datareporting.healthreport.about.reportUrl')
        self.datareporting_healthreport_document_server_uri                      = d.get('datareporting.healthreport.documentServerURI')
        self.datareporting_healthreport_logging_console_enabled                  = d.get('datareporting.healthreport.logging.consoleEnabled')
        self.datareporting_healthreport_service_enabled                          = d.get('datareporting.healthreport.service.enabled')
        self.datareporting_healthreport_service_first_run                        = d.get('datareporting.healthreport.service.firstRun')
        self.datareporting_healthreport_upload_enabled                           = d.get('datareporting.healthreport.uploadEnabled')
        self.datareporting_policy_data_submission_enabled                        = d.get('datareporting.policy.dataSubmissionEnabled')
        self.datareporting_policy_data_submission_policy_accepted                = d.get('datareporting.policy.dataSubmissionPolicyAccepted')
        self.datareporting_policy_data_submission_policy_bypass_notification     = d.get('datareporting.policy.dataSubmissionPolicyBypassNotification')
        self.devtools_console_stdout_chrome                                      = d.get('devtools.console.stdout.chrome')
        self.devtools_errorconsole_enabled                                       = d.get('devtools.errorconsole.enabled')
        self.distribution_ini_file_exists_appversion                             = d.get('distribution.iniFile.exists.appversion')
        self.distribution_ini_file_exists_value                                  = d.get('distribution.iniFile.exists.value')
        self.doh_rollout_balrog_migration_done                                   = d.get('doh-rollout.balrog-migration-done')
        self.doh_rollout_done_first_run                                          = d.get('doh-rollout.doneFirstRun')
        self.dom_disable_beforeunload                                            = d.get('dom.disable_beforeunload')
        self.dom_disable_open_during_load                                        = d.get('dom.disable_open_during_load')
        self.dom_file_create_in_child                                            = d.get('dom.file.createInChild')
        self.dom_ipc_report_process_hangs                                        = d.get('dom.ipc.reportProcessHangs')
        self.dom_max_chrome_script_run_time                                      = d.get('dom.max_chrome_script_run_time')
        self.dom_max_script_run_time                                             = d.get('dom.max_script_run_time')
        self.dom_push_connection_enabled                                         = d.get('dom.push.connection.enabled')
        self.dom_report_all_js_exceptions                                        = d.get('dom.report_all_js_exceptions')
        self.dom_webdriver_enabled                                               = d.get('dom.webdriver.enabled')
        self.extensions_active_theme_id                                          = d.get('extensions.activeThemeID')
        self.extensions_auto_disable_scopes                                      = d.get('extensions.autoDisableScopes')
        self.extensions_blocklist_enabled                                        = d.get('extensions.blocklist.enabled')
        self.extensions_blocklist_ping_count_version                             = d.get('extensions.blocklist.pingCountVersion')
        self.extensions_check_compatibility_nightly                              = d.get('extensions.checkCompatibility.nightly')
        self.extensions_database_schema                                          = d.get('extensions.databaseSchema')
        self.extensions_enabled_scopes                                           = d.get('extensions.enabledScopes')
        self.extensions_get_addons_cache_enabled                                 = d.get('extensions.getAddons.cache.enabled')
        self.extensions_get_addons_database_schema                               = d.get('extensions.getAddons.databaseSchema')
        self.extensions_get_addons_discovery_api_url                             = d.get('extensions.getAddons.discovery.api_url')
        self.extensions_incognito_migrated                                       = d.get('extensions.incognito.migrated')
        self.extensions_install_distro_addons                                    = d.get('extensions.installDistroAddons')
        self.extensions_last_app_build_id                                        = d.get('extensions.lastAppBuildId')
        self.extensions_last_app_version                                         = d.get('extensions.lastAppVersion')
        self.extensions_last_platform_version                                    = d.get('extensions.lastPlatformVersion')
        self.extensions_pending_operations                                       = d.get('extensions.pendingOperations')
        self.extensions_show_mismatch_ui                                         = d.get('extensions.showMismatchUI')
        self.extensions_system_addon_set                                         = d.get('extensions.systemAddonSet')
        self.extensions_update_enabled                                           = d.get('extensions.update.enabled')
        self.extensions_update_notify_user                                       = d.get('extensions.update.notifyUser')
        self.extensions_webcompat_enable_picture_in_picture_overrides            = d.get('extensions.webcompat.enable_picture_in_picture_overrides')
        self.extensions_webcompat_enable_shims                                   = d.get('extensions.webcompat.enable_shims')
        self.extensions_webcompat_perform_injections                             = d.get('extensions.webcompat.perform_injections')
        self.extensions_webcompat_perform_ua_overrides                           = d.get('extensions.webcompat.perform_ua_overrides')
        self.extensions_webextensions_uuids                                      = d.get('extensions.webextensions.uuids')
        self.focusmanager_testmode                                               = d.get('focusmanager.testmode')
        self.general_useragent_updates_enabled                                   = d.get('general.useragent.updates.enabled')
        self.general_warn_on_about_config                                        = d.get('general.warnOnAboutConfig')
        self.geo_provider_testing                                                = d.get('geo.provider.testing')
        self.geo_wifi_scan                                                       = d.get('geo.wifi.scan')
        self.hangmonitor_timeout                                                 = d.get('hangmonitor.timeout')
        self.intl_accept_languages                                               = d.get('intl.accept_languages')
        self.marionatte                                                          = d.get('marionatte')
        self.marionette_content_listener                                         = d.get('marionette.contentListener')
        self.marionette_enabled                                                  = d.get('marionette.enabled')
        self.marionette_port                                                     = d.get('marionette.port')
        self.media_gmp_manager_build_id                                          = d.get('media.gmp-manager.buildID')
        self.media_gmp_manager_last_check                                        = d.get('media.gmp-manager.lastCheck')
        self.media_gmp_manager_update_enabled                                    = d.get('media.gmp-manager.updateEnabled')
        self.media_gmp_storage_version_observed                                  = d.get('media.gmp.storage.version.observed')
        self.media_peerconnection_enabled                                        = d.get('media.peerconnection.enabled')
        self.network_captive_portal_service_enabled                              = d.get('network.captive-portal-service.enabled')
        self.network_http_phishy_userpass_length                                 = d.get('network.http.phishy-userpass-length')
        self.network_manage_offline_status                                       = d.get('network.manage-offline-status')
        self.network_sntp_pools                                                  = d.get('network.sntp.pools')
        self.network_stricttransportsecurity_preloadlist                         = d.get('network.stricttransportsecurity.preloadlist')
        self.network_trr_blocklist_cleanup_done                                  = d.get('network.trr.blocklist_cleanup_done')
        self.offline_apps_allow_by_default                                       = d.get('offline-apps.allow_by_default')
        self.pdfjs_enabled_cache_state                                           = d.get('pdfjs.enabledCache.state')
        self.pdfjs_migration_version                                             = d.get('pdfjs.migrationVersion')
        self.plugin_state_flash                                                  = d.get('plugin.state.flash')
        self.privacy_sanitize_pending                                            = d.get('privacy.sanitize.pending')
        self.prompts_tab_modal_enabled                                           = d.get('prompts.tab_modal.enabled')
        self.security_cert_pinning_enforcement_level                             = d.get('security.cert_pinning.enforcement_level')
        self.security_certerrors_mitm_priming_enabled                            = d.get('security.certerrors.mitm.priming.enabled')
        self.security_csp_enable                                                 = d.get('security.csp.enable')
        self.security_fileuri_origin_policy                                      = d.get('security.fileuri.origin_policy')
        self.security_fileuri_strict_origin_policy                               = d.get('security.fileuri.strict_origin_policy')
        self.security_notification_enable_delay                                  = d.get('security.notification_enable_delay')
        self.security_remote_settings_crlite_filters_checked                     = d.get('security.remote_settings.crlite_filters.checked')
        self.security_remote_settings_intermediates_checked                      = d.get('security.remote_settings.intermediates.checked')
        self.security_sandbox_content_temp_dir_suffix                            = d.get('security.sandbox.content.tempDirSuffix')
        self.security_sandbox_plugin_temp_dir_suffix                             = d.get('security.sandbox.plugin.tempDirSuffix')
        self.services_blocklist_pinning_checked                                  = d.get('services.blocklist.pinning.checked')
        self.services_settings_clock_skew_seconds                                = d.get('services.settings.clock_skew_seconds')
        self.services_settings_last_etag                                         = d.get('services.settings.last_etag')
        self.services_settings_last_update_seconds                               = d.get('services.settings.last_update_seconds')
        self.services_settings_main_anti_tracking_url_decoration_last_check      = d.get('services.settings.main.anti-tracking-url-decoration.last_check')
        self.services_settings_main_cfr_fxa_last_check                           = d.get('services.settings.main.cfr-fxa.last_check')
        self.services_settings_main_cfr_last_check                               = d.get('services.settings.main.cfr.last_check')
        self.services_settings_main_fxmonitor_breaches_last_check                = d.get('services.settings.main.fxmonitor-breaches.last_check')
        self.services_settings_main_hijack_blocklists_last_check                 = d.get('services.settings.main.hijack-blocklists.last_check')
        self.services_settings_main_language_dictionaries_last_check             = d.get('services.settings.main.language-dictionaries.last_check')
        self.services_settings_main_message_groups_last_check                    = d.get('services.settings.main.message-groups.last_check')
        self.services_settings_main_normandy_recipes_capabilities_last_check     = d.get('services.settings.main.normandy-recipes-capabilities.last_check')
        self.services_settings_main_password_recipes_last_check                  = d.get('services.settings.main.password-recipes.last_check')
        self.services_settings_main_pioneer_study_addons_v1_last_check           = d.get('services.settings.main.pioneer-study-addons-v1.last_check')
        self.services_settings_main_public_suffix_list_last_check                = d.get('services.settings.main.public-suffix-list.last_check')
        self.services_settings_main_search_config_last_check                     = d.get('services.settings.main.search-config.last_check')
        self.services_settings_main_search_default_override_allowlist_last_check = d.get('services.settings.main.search-default-override-allowlist.last_check')
        self.services_settings_main_search_telemetry_last_check                  = d.get('services.settings.main.search-telemetry.last_check')
        self.services_settings_main_sites_classification_last_check              = d.get('services.settings.main.sites-classification.last_check')
        self.services_settings_main_top_sites_last_check                         = d.get('services.settings.main.top-sites.last_check')
        self.services_settings_main_url_classifier_skip_urls_last_check          = d.get('services.settings.main.url-classifier-skip-urls.last_check')
        self.services_settings_main_whats_new_panel_last_check                   = d.get('services.settings.main.whats-new-panel.last_check')
        self.services_settings_security_onecrl_checked                           = d.get('services.settings.security.onecrl.checked')
        self.services_settings_server                                            = d.get('services.settings.server')
        self.signon_autofill_forms                                               = d.get('signon.autofillForms')
        self.signon_remember_signons                                             = d.get('signon.rememberSignons')
        self.startup_homepage_welcome_url                                        = d.get('startup.homepage_welcome_url')
        self.startup_homepage_welcome_url_additional                             = d.get('startup.homepage_welcome_url.additional')
        self.toolkit_networkmanager_disable                                      = d.get('toolkit.networkmanager.disable')
        self.toolkit_startup_last_success                                        = d.get('toolkit.startup.last_success')
        self.toolkit_startup_max_resumed_crashes                                 = d.get('toolkit.startup.max_resumed_crashes')
        self.toolkit_telemetry_cached_client_id                                  = d.get('toolkit.telemetry.cachedClientID')
        self.toolkit_telemetry_pioneer_new_studies_available                     = d.get('toolkit.telemetry.pioneer-new-studies-available')
        self.toolkit_telemetry_previous_build_id                                 = d.get('toolkit.telemetry.previousBuildID')
        self.toolkit_telemetry_prompted                                          = d.get('toolkit.telemetry.prompted')
        self.toolkit_telemetry_rejected                                          = d.get('toolkit.telemetry.rejected')
        self.toolkit_telemetry_reportingpolicy_first_run                         = d.get('toolkit.telemetry.reportingpolicy.firstRun')
        self.toolkit_telemetry_server                                            = d.get('toolkit.telemetry.server')
        self.use_automation_extension                                            = d.get('useAutomationExtension')
        self.webdriver_accept_untrusted_certs                                    = d.get('webdriver_accept_untrusted_certs')
        self.webdriver_assume_untrusted_issuer                                   = d.get('webdriver_assume_untrusted_issuer')
        self.webdriver_enable_native_events                                      = d.get('webdriver_enable_native_events')
        self.xpinstall_signatures_required                                       = d.get('xpinstall.signatures.required')
        self.xpinstall_whitelist_required                                        = d.get('xpinstall.whitelist.required')

        self.extensions_webextensions_extension_storage_idb_migrated_foxyproxy_eric_h_jung   = d.get('extensions.webextensions.ExtensionStorageIDB.migrated.foxyproxy@eric.h.jung')
        self.extensions_webextensions_extension_storage_idb_migrated_screenshots_mozilla_org = d.get('extensions.webextensions.ExtensionStorageIDB.migrated.screenshots@mozilla.org')

# ---------------------------------------------------------------------------------------------------------------------------------------- #