import pytest
from app.services.data_tranformer import PokemonDataTransformer
from app.models import PokemonData, Pokemon


@pytest.fixture
def sample_raw_data():
    return {
        "id": 25,
        "name": "pikachu",
        "types": [
            {"type": {"name": "electric"}}
        ],
        "moves": [
            {"move": {"name": "thunder"}},
            {"move": {"name": "quick-attack"}},
            {"move": {"name": "thunderbolt"}},
            {"move": {"name": "volt-tackle"}},
            {"move": {"name": "extra-move"}}
        ],
        "stats": [
            {"base_stat": 35, "stat": {"name": "hp"}},
            {"base_stat": 55, "stat": {"name": "attack"}},
            {"base_stat": 40, "stat": {"name": "defense"}},
            {"base_stat": 50, "stat": {"name": "special-attack"}},
            {"base_stat": 50, "stat": {"name": "special-defense"}},
            {"base_stat": 90, "stat": {"name": "speed"}}
        ]
    }



def test_transform_to_pokemon(sample_raw_data):
    pokemon_data = PokemonDataTransformer.transform_to_pokemon_data(sample_raw_data)

    result = PokemonDataTransformer.transform_to_pokemon(pokemon_data)

    assert isinstance(result, Pokemon), "The transformer should create pydentic instance"
    assert result.id == 25, "as the fixture data - sample_raw_data "
    assert result.name == "pikachu"
    assert result.hp == 35
    assert result.attack == 55
    assert result.defense == 40
    assert result.special_attack == 50
    assert result.special_defense == 50
    assert result.speed == 90
    assert result.types == ["electric"]
    assert len(result.moves) == 4


def test_extract_stats_empty_data():
    result = PokemonDataTransformer._extract_stats({})
    assert result == {}


def test_extract_stats_missing_stats():
    result = PokemonDataTransformer._extract_stats({"other_field": "value"})
    assert result == {}