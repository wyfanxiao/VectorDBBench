from typing import Annotated, Unpack

import click
from pydantic import SecretStr

from ....cli.cli import (
    CommonTypedDict,
    cli,
    click_parameter_decorators_from_typed_dict,
    run,
    get_custom_case_config
)
from .. import DB



class AliyunElasticSearchTypedDict(CommonTypedDict):
    host: Annotated[
        str, click.option("--host", type=str, help="host",required=True)
    ]
    port: Annotated[
        int, click.option("--port", type=int, help="port", required=True)
    ]
    user: Annotated[
        str, click.option("--user", type=str, help="username",default='',required=False)
    ]
    password: Annotated[
        str, click.option("--password", type=str,
                          help="database password", default='',required=False)
    ]
    ef_construction: Annotated[
        int, click.option("--ef_construction", type=int, help="efConstruction", required=True)
    ]
    m: Annotated[
        int, click.option("--m", type=int, help="m", required=True)
    ]
    num_candidates: Annotated[
        int, click.option("--num_candidates", type=int, help="num_candidates", required=True)
    ]
    number_of_shards: Annotated[
        int, click.option("--number_of_shards", type=int, help="number of shards",default=1,required=False)
    ]
    number_of_replicas: Annotated[
        int, click.option("--number_of_replicas", type=int, help="number of replicas",default=1,required=False)
    ]

class AliyunElasticSearchHNSWTypedDict(CommonTypedDict, AliyunElasticSearchTypedDict):
    ...


@cli.command()
@click_parameter_decorators_from_typed_dict(AliyunElasticSearchHNSWTypedDict)
def ElasticSearch(**parameters: Unpack[AliyunElasticSearchHNSWTypedDict]):
    from .config import ElasticsearchConfig
    from ..elastic_cloud.config import ElasticCloudIndexConfig
    from ..api import IndexType,MetricType

    parameters["custom_case"] = get_custom_case_config(parameters)

    run(
        db=DB.Elasticsearch,
        db_config=ElasticsearchConfig(
            host=parameters["host"],
            port=parameters["port"],
            user=parameters["user"],
            password=SecretStr(parameters["password"]),
        ),
        db_case_config=ElasticCloudIndexConfig(
            index=IndexType.ES_HNSW,
            efConstruction=parameters["ef_construction"],
            M=parameters["m"],
            num_candidates=parameters["num_candidates"],
            number_of_shards=parameters['number_of_shards'],
            number_of_replicas=parameters['number_of_replicas']
        ),
        **parameters,
    )
