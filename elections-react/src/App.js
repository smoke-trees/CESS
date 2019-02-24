import React, { Component } from 'react';
import './App.css';
import web3 from './web3';
import election from './election';

class App extends Component {
    state = {
        candidateId: '',
        message: 'Ready to vote.',
        bjpVotes: 0,
        incVotes: 0,
        aapVotes: 0,
        sipVotes: 0,
        notaVotes: 0
    };

    async componentDidMount() {
        //const accounts = await web3.eth.getAccounts();
        this.setState({
            bjpVotes: await election.methods.candidates(1).call(),
            incVotes: await election.methods.candidates(2).call(),
            aapVotes: await election.methods.candidates(3).call(),
            sipVotes: await election.methods.candidates(4).call(),
            notaVotes: await election.methods.candidates(5).call()
        });
    }

    onVote = async event => {
        event.preventDefault();
        const accounts = await web3.eth.getAccounts();
        this.setState({message: 'Casting your vote... Please wait for 15-30 seconds.'});
        try {
            await election.methods.vote(this.state.candidateId).send({from: accounts[0]});
        } catch (e) {
            if (e.toString().includes('revert')) {
                this.setState({ message: 'You may not vote twice.'});
                return
            }
            this.setState({ message: 'Your vote has been successfully cast.'})
        }

        this.setState({message: 'Transaction successfully processed.'});
    };

    render() {
        return (
            <div
                className={'parent_div'}>
                <h1>Vote for your candidate</h1>

                <hr/>
                <div className='form-updates'>
                    <form onSubmit={this.onVote}>
                        <h4>Vote for your preferred candidate. The available options are:</h4>
                        <ol>
                            <li>BJP: {this.state.bjpVotes.voteCount} votes</li>
                            <li>INC: {this.state.incVotes.voteCount} votes</li>
                            <li>AAP: {this.state.aapVotes.voteCount} votes</li>
                            <li>SIP: {this.state.sipVotes.voteCount} votes</li>
                            <li>NOTA: {this.state.notaVotes.voteCount} votes</li>
                        </ol>

                        <div>
                            <label>Serial of the candidate you want to vote for: </label>
                            <input
                                value={this.state.candidateId}
                                onChange={event => this.setState({candidateId: event.target.value})}
                                className='form-control'
                            />
                        </div>
                        <button
                            className='btn btn-lg btn-primary btn-block'>Vote</button>
                    </form>
                </div>

                <hr/>

                <h2>{this.state.message}</h2>

                <hr/>
            </div>
        );
    }
}

export default App;
