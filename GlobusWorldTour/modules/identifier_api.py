import json

from globus_sdk import (AccessTokenAuthorizer, ClientCredentialsAuthorizer,
                        RefreshTokenAuthorizer, NativeAppAuthClient)
from globus_sdk.base import BaseClient, safe_stringify
from globus_sdk.exc import GlobusAPIError

# from identifier_client.login import extract_and_save_tokens

_namespace_properties = ['description', 'display_name',
                         'creators', 'admins', 'identifier_admins',
                         'provider_type', 'provider_config']

_namespace_json_props = ['creators', 'admins', 'identifier_admins',
                         'provider_config']

_identifier_properties = ['location', 'checksum', 'identifier',
                          'checksum_function', 'metadata', 'visible_to']
_identifier_json_props = ['metadata', 'visible_to']


def identifier_client(config, **kwargs):
    app_name = 'identifier_client'
    base_url = config['client']['service_url']
    client_id = config['client']['client_id']
    access_token = config['tokens']['access_token']
    at_expires = int(config['tokens']['access_token_expires'])
    refresh_token = config['tokens']['refresh_token']
    if not (refresh_token and access_token):
        raise IdentifierNotLoggedIn("Missing tokens")

    def _on_refresh(tkn):
        # extract_and_save_tokens(tkn, config)
        pass

    authorizer_client = NativeAppAuthClient(client_id, app_name=app_name)
    authorizer = RefreshTokenAuthorizer(
        refresh_token,
        authorizer_client,
        access_token,
        at_expires,
        on_refresh=_on_refresh,
    )

    return IdentifierClient(
        "identifier",
        base_url=base_url,
        app_name=app_name,
        authorizer=authorizer,
        **kwargs
    )


class IdentifierClientError(GlobusAPIError):
    pass


class IdentifierNotLoggedIn(IdentifierClientError):
    def __init__(self, err_msg):
        self.message = err_msg


def _split_dict(in_dict, key_names):
    """
    Split a dict into two dicts. Keys in key_names go into the new dict if
    their value is present and not None.
    return (updated original dict, new dict)
    """
    new_dict = {}
    for key_name in key_names:
        val = in_dict.pop(key_name, None)
        if val is not None:
            new_dict[key_name] = val
    return in_dict, new_dict


def _json_parse_args(in_dict, key_names):
    for key_name in key_names:
        val = in_dict.pop(key_name, None)
        if val is not None:
            val = json.loads(val)
            in_dict[key_name] = val
    return in_dict


class IdentifierClient(BaseClient):
    allowed_authorizer_types = (
        AccessTokenAuthorizer,
        RefreshTokenAuthorizer,
        ClientCredentialsAuthorizer)

    error_class = IdentifierClientError

    def __init__(self, *args, **kwargs):
        if 'base_url' not in kwargs:
            kwargs['base_url'] = 'https://identifiers.globus.org/'
        BaseClient.__init__(self, "identifiers", *args, **kwargs)

    def create_namespace(self, **kwargs):
        """
        ``POST /namespace``

        **Parameters**
          ``display-name`` (*string*)
          display_name of the new namespace
          ``description`` (*string*)
          description of the new namespace
          ``creators`` (*string*)
          The UUID for a Globus Group who's members are "
                      "permitted to add to this namespace
          ``admins`` (*string*)
          The UUID for a Globus Group who's members are "
                      "permitted to perform administrative functions on "
                      "this namespace
          ``provider-type`` (*string*)
          The type of the provider used for minting "
                      "external identifiers
          ``provider-config`` (*string*)
          Configuration for the provider used for "
                      "minting external identfiers in JSON format

        """
        kwargs = _json_parse_args(kwargs, _namespace_json_props)
        kwargs, body = _split_dict(kwargs, _namespace_properties)
        self.logger.info(
            "IdentifierClient.create_namespace({}, ...)".format(
                body.get('display_name')))
        path = self.qjoin_path("namespace")
        return self.post(path, body, params=kwargs)

    def update_namespace(self, namespace_id, **kwargs):
        """
        ``PATCH /namespace/<id>``

        ** Parameters **
          ``namespace_id`` (*string*)
          The id for the namespace to update
          ``display_name`` (*string*)
          The updated display name of the namespace
          ``description`` (*string*)
          description of the new namespace
          ``creators`` (*string*)
          The Principal URN for a Globus Group who's members are
          permitted to add to this namespace
          ``admins`` (*string*)
          The Principal URN for a Globus Group who's members are
          permitted to perform administrative functions on this namespace
          ``provider-type`` (*string*)
          The type of the provider used for minting external identifiers
          ``provider-config`` (*dict*)
          Configuration for the provider used for minting external
          identfiers in JSON format

        """
        kwargs = _json_parse_args(kwargs, _namespace_json_props)
        kwargs, body = _split_dict(kwargs, _namespace_properties)
        self.logger.info(
            "IdentifierClient.update_namespace({}, ...)".format(namespace_id))
        path = self.qjoin_path("namespace", safe_stringify(namespace_id))
        return self.put(path, body, params=kwargs)

    def get_namespace(self, namespace_id, **params):
        """
        ``GET /namespace/<namespace_id>

        ** Parameters **
          ``namespace_id`` (*string*)
          The id for the namespace to retrieve
        """
        path = self.qjoin_path("namespace", safe_stringify(namespace_id))
        self.logger.info(
            "IdentifierClient.get_namespace({})".format(namespace_id))
        return self.get(path, params=params)

    def delete_namespace(self, namespace_id, **params):
        """
        ``DELETE /namespace/<namespace_id>

        ** Parameters **
          ``namespace_id`` (*string*)
          The id for the namespace to remove
        """
        path = self.qjoin_path("namespace", safe_stringify(namespace_id))
        self.logger.info(
            "IdentifierClient.delete_namespace({})".format(namespace_id))
        return self.delete(path, params=params)

    def create_identifier(self, **kwargs):
        """
        ``POST /namespace/<namespace_id>/IdentifierClient

        ** Parameters **
          ``namespace`` (*string*)
          The UUID for the namespace in which to add the identifier
          ``identifier`` (*string / URL*)
          An identifier value from an external provider which may be "
          used to lookup the data
          ``location`` (* array of string*)
          A list of URLs from which the data referred to by the identifier
          may be retrieved
          ``checksums`` (*array of object*)
          A list of objects, each containing the property ``value``
          indicting the value generated by the checksum function and
          the property ``function`` which indicates which of the known
          checksum functions was used for generating the value
          ``properties`` (*dict*)
          Additional properties associated with the identifier

        """
        # kwargs = _json_parse_args(kwargs, _identifier_json_props)
        kwargs, body = _split_dict(kwargs, _identifier_properties)
        self.logger.info('IdentifierClient.create_identifier({}, ...)'.format(
            body.get('namespace_id')))
        path = self.qjoin_path(
            'namespace/{}/identifier'.format(kwargs['namespace']))
        return self.post(path, body, params=kwargs)

    def get_identifier(self, identifier_id, **params):
        """
        ``GET /id/<identifier_id>

        ** Parameters **
        ``identifier_id`` The identification url for the identifier
        """
        path = self.qjoin_path('id', safe_stringify(identifier_id))
        self.logger.info('IdentifierClient.get_identifier({})'.format(
            identifier_id))
        return self.get(path, params=params)

    def update_identifier(self, identifier_id, **kwargs):
        """
        ``PATCH /namespace/<namespace_id>/IdentifierClient

        ** Parameters **
          ``identifier_id`` (*string*)
          The identification url for the identifier
          ``identifier`` (*string / URL*)
          An identifier value from an external provider which may be "
          used to lookup the data
          ``location`` (* array of string*)
          A list of URLs from which the data referred to by the identifier
          may be retrieved
          ``checksums`` (*array of object*)
          A list of objects, each containing the property ``value``
          indicting the value generated by the checksum function and
          the property ``function`` which indicates which of the known
          checksum functions was used for generating the value
          ``properties`` (*dict*)
          Additional properties associated with the identifier

        """
        kwargs = _json_parse_args(kwargs, _identifier_json_props)
        kwargs, body = _split_dict(kwargs, _identifier_properties)
        self.logger.info('IdentifierClient.update_identifier({}, ...)'.format(
            body.get('identifier_id')))
        path = self.qjoin_path('id', identifier_id)
        return self.put(path, body, params=kwargs)
