import neat
import os
import pickle
from flappy_bird import Game, Bird, Pipe

def eval_genomes(genomes, config):
    nets = []
    birds = []
    games = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(200, 300))
        games.append(Game())
        genome.fitness = 0

    while len(birds) > 0:
        for i, bird in enumerate(birds):
            # Get the closest pipe
            closest_pipe = None
            min_distance = float('inf')
            for pipe in games[i].pipes:
                distance = pipe.x - bird.x
                if 0 < distance < min_distance:
                    min_distance = distance
                    closest_pipe = pipe

            # Prepare inputs for the neural network
            if closest_pipe:
                inputs = [
                    bird.y / 600,  # Normalized bird height
                    closest_pipe.gap_y / 600,  # Normalized gap center
                    (closest_pipe.x - bird.x) / 400,  # Normalized distance to pipe
                    bird.velocity / 10  # Normalized velocity
                ]
            else:
                inputs = [bird.y / 600, 0.5, 1, bird.velocity / 10]

            # Get output from neural network
            output = nets[i].activate(inputs)
            
            # Flap if output is greater than 0.5
            if output[0] > 0.5:
                bird.flap()

            # Update game state
            games[i].update()
            
            # Increase fitness for surviving
            genomes[i][1].fitness += 0.1

            # Check if bird passed a pipe
            for pipe in games[i].pipes:
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    genomes[i][1].fitness += 1.0

            # Check if bird is dead
            if (bird.y < 0 or bird.y > 600 or
                any(bird.rect.colliderect(pipe.top_rect) or 
                    bird.rect.colliderect(pipe.bottom_rect) 
                    for pipe in games[i].pipes)):
                nets.pop(i)
                birds.pop(i)
                games.pop(i)
                genomes.pop(i)
                break

def run_neat(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes, 50)
    
    # Save the best genome
    with open("best_bird.pickle", "wb") as f:
        pickle.dump(winner, f)

def play_best_bird(config_path):
    with open("best_bird.pickle", "rb") as f:
        genome = pickle.load(f)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = Game()
    bird = Bird(200, 300)

    while True:
        # Get the closest pipe
        closest_pipe = None
        min_distance = float('inf')
        for pipe in game.pipes:
            distance = pipe.x - bird.x
            if 0 < distance < min_distance:
                min_distance = distance
                closest_pipe = pipe

        # Prepare inputs for the neural network
        if closest_pipe:
            inputs = [
                bird.y / 600,
                closest_pipe.gap_y / 600,
                (closest_pipe.x - bird.x) / 400,
                bird.velocity / 10
            ]
        else:
            inputs = [bird.y / 600, 0.5, 1, bird.velocity / 10]

        # Get output from neural network
        output = net.activate(inputs)
        
        # Flap if output is greater than 0.5
        if output[0] > 0.5:
            bird.flap()

        # Update game state
        game.update()
        game.draw()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path) 